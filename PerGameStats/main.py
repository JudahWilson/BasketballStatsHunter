r''' TODO
- all pgs,pgqs,pghs due to team_br_id problem
    -/ json
    - db
- import OT for all tables
- 1980 html missing last several games-- impacts pgs,tgs
- download pbp html
- PerGameStats/corrections/202008150POR
  - manual user input bc its unavailable
'''
#region IMPORTS and CONFIG
import json
import pandas as pd
import bs4
import re
import traceback
import numpy as np
import sys
import TeamGameStats
import os, re
import pyperclip
import TeamGameStats.helper
import TeamGameHalfStats.helper
import TeamGameQuarterStats.helper
import PlayerGameStats.helper
import PlayerGameHalfStats.helper
import PlayerGameQuarterStats.helper
from pgs_helper import *
import re
import argparse
import warnings
from sqlalchemy import text
# from sqlalchemy.exc import RemovedIn20Warning
warnings.filterwarnings("ignore", category=UserWarning)
# warnings.filterwarnings("ignore", category=RemovedIn20Warning)
import duckdb
import pdb
import questionary
from questionary import Choice, Form
#endregion


testQL = None # TODO test the testing done by testQL


def args():
    #################################    
    # region callbacks
    #################################    
    def set_format_arg():
        choices=[Choice('json', checked=True), Choice('html'), Choice('db'), Choice('rmjson'), Choice('lsjson'), Choice('lsdb'), Choice('rmdb')]
        answer = questionary.select(
            'Select a format',
            choices=choices,
            use_shortcuts=True,
        ).ask()
        
        if answer:
            args.format = answer
        
    
    
    def set_table_arg(optional: bool=False):
        """Set the tables arg manually"""
        choices=[
            Choice('All', checked=True),
            Choice('teamgamestats (tgs)', value='tgs'),
            Choice('teamgamequarterstats (tgqs)', value='tgqs'),
            Choice('teamgamehalfstats (tghs)', value='tghs'),
            Choice('playergamestats (pgs)', value='pgs'),
            Choice('playergamequarterstats (pgqs)', value='pgqs'),
            Choice('playergamehalfstats (pghs)', value='pghs'),
        ]
        if optional:
            choices += [Choice('None', value=None)]
        
        answer = questionary.checkbox(
            'Select a table',
            choices=choices,
        ).ask()
        
        if answer:
            if 'All' in answer:
                # Select each option manually
                args.tables = 'tgs,tgqs,tghs,pgs,pgqs,pghs'
            else:
                # Convert list to CSV as is expected
                if isinstance(answer, list):
                    answer = ','.join(answer)              
    
    
    def set_seasons_range_arg(optional=True):
        """Set seasons_arg manually"""
        answer = questionary.text(
            'Enter the seasons range (YYYY-YYYY)',
            validate=lambda text: re.match(r'^\d{4}-\d{4}$', text) or re.match(r'^\d{4}$', text) or text == '',
            default='',
        ).ask()
    #endregion
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('format', help='json, html, db, rmjson (to remove json files that you are finished with)', 
                        choices=['json', 'db', 'html','rmjson','lsjson','lsdb','rmdb'], nargs='?')
    parser.add_argument('seasons_range', type=str, nargs='?',
                        help='Oldest season\'s start year to the most recent season\'s start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]')
    parser.add_argument('tables', help=''''[CSV] teamgamestats' ('tgs')
        'teamgamequarterstats' ('tgqs')
        'teamgamehalfstats' ('tghs')
        'playergamestats' ('pgs')
        'playergamequarterstats' ('pgqs')
        'playergamehalfstats' ('pghs')''',
        nargs='?')

    args = parser.parse_args()
    
    if not args.format:
        set_format_arg()
    
    if args.seasons_range:
        if not re.match(r'^\d{4}$', args.seasons_range) and not re.match(r'^\d{4}-\d{4}$', args.seasons_range):
            parser.error('Invalid seasons range. Must be in the format YYYY-YYYY (both years are the starting year of their season)')
    
    if args.format in ['json','db','rmjson'] and args.tables == []:
        set_table_arg()
            
    if args.format in ['json','db','rmjson','lsjson','lsdb'] and not args.seasons_range:
        set_seasons_range_arg(optional=True)
        
    if args.tables:
        for a in args.tables.split(','):
            if a not in [
                'teamgamestats','tgs',
                'teamgamequarterstats','tgqs',
                'teamgamehalfstats','tghs',
                'playergamestats','pgs',
                'playergamequarterstats','pgqs',
                'playergamehalfstats','pghs',
            ]:
                parser.error(f'''Invalid table name: {a}.
        Valid table names are:
            'teamgamestats' ('tgs')
            'teamgamequarterstats' ('tgqs')
            'teamgamehalfstats' ('tghs')
            'playergamestats' ('pgs')
            'playergamequarterstats' ('pgqs')
            'playergamehalfstats' ('pghs')''')
    return args
args = args()


    
def getTeamGameStatsHTML(start_year=None, stop_year=1946, singular_game_br_id=False, override_existing_html=False):
    
    if override_existing_html:
        if input('THIS IS OVERRIDING EXISTING HTML RATHER THAN PICKING UP WHERE THE SCRIPT LEFT OFF.\nInput "y" to continue:') == 'y':
            print('Proceeding script...')
        else:
            print('Set override_existing_html to False (or omit the argument) in the call to getTeamGameStatsHTML')
                
    if singular_game_br_id:
        year = int(singular_game_br_id[:4])
        SQL = f"""SELECT * FROM Games
        where br_id = '{singular_game_br_id}'"""
        game = pd.read_sql(sql=SQL, con=engine)
        if not game.empty:
            game = game.iloc[0]
            save_html(game, year)
            return
        else:
            print(f'Game {singular_game_br_id} not found in the database')
            return
    
    else:
        start_year = int(start_year)
        stop_year = int(stop_year)

        year = start_year
        while year >= stop_year:
            SQL = f"""SELECT * FROM Games 
            where date_time >= '{year}-09-01'
            and date_time < '{year + 1}-09-01'
            order by date_time desc"""
            
            games = pd.read_sql(sql=SQL, con=engine)
            
            # Catch up to where we left off
            left_off_game_br_id = None
            for folder in os.listdir('html'):
                if folder.isnumeric() and int(folder) > year:
                    continue
                elif folder == '.gitkeep':
                    continue
                else:
                    # If contents in folder 
                    if os.listdir(f'html/{folder}'):
                        # Get the last file ascending
                        files = os.listdir(f'html/{folder}')
                        files.sort()
                        last_file = files[0]
                        left_off_game_br_id = last_file.split('-')[1].split('.')[0]
                    
            for ind, game in games.iterrows():
                if not override_existing_html:
                    if left_off_game_br_id:
                        # Pick up where we left off if we have to
                        if left_off_game_br_id == game['br_id']:
                            # Skip to the next game
                            if left_off_game_br_id:
                                left_off_game_br_id = False
                        continue
                
                with open('lastgamehtml.txt','w') as f:
                    f.write(game.br_id)
                save_html(game, year)
                
                print('SAVED')
            print('YEAR ' + str(year) + ' COMPLETE')
            year -= 1
    print('EXITED')



def setTeamGameStatsJSON(begin_year=None, stop_year=1946,get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False):

    begin_year = int(begin_year)
    stop_year = int(stop_year)

    year = begin_year

    # Get the latest game data processed. The script will have left off at the game furthest in the past
    game_leftoff_at = get_last_processed_game('TeamGameStats')
    game_quarter_leftoff_at = get_last_processed_game('TeamGameQuarterStats')
    game_half_leftoff_at = get_last_processed_game('TeamGameHalfStats')
    
    while year >= stop_year:
        # DB Games
        SQL = f"""SELECT * FROM Games 
                where date_time >= '{year}-09-01'
                and date_time < '{year + 1}-09-01'
                order by date_time desc"""
                
        try:
            games = pd.read_sql(sql=SQL, con=engine)
        except Exception as e:
            print('----------------')
            print('ERROR GETTING GAME FROM DB!: ' + str(e) + '\n')
            traceback.print_exc()
            print('\nGame details:')
            print(games)
            print('----------------')
            breakpoint()
        
        for file in os.listdir(f'html/{year}'):
            
            if file.endswith('.html'):
                
                #region DATA PREP
                game = games[games['br_id'] == file.split('-')[1].split('.')[0]].iloc[0]

                # What should we skip, if at all?
                skip_TeamGameStats = is_game_processed(game.br_id, game_leftoff_at)
                skip_TeamGameQuarterStats = is_game_processed(game.br_id, game_quarter_leftoff_at)
                skip_TeamGameHalfStats = is_game_processed(game.br_id, game_half_leftoff_at)
                
                # If data should be skipped for all specified tables, continue to the next file 
                if (get_TeamGameStats == False or skip_TeamGameStats) \
                and (get_TeamGameQuarterStats == False or skip_TeamGameQuarterStats) \
                and (get_TeamGameHalfStats == False or skip_TeamGameHalfStats):
                    continue
            
                print(file)

                with open(f'html/{year}/{file}', 'r', encoding='utf-8') as f:
                    html = f.read()

                soup = bs4.BeautifulSoup(html, 'html.parser')

                four_factors = get_tag_having_text(soup, 'table', 'Four Factors Table')

                if len(soup.select('#inactive_players')) > 0:
                    inactive_players = soup.select('#inactive_players')[0]
                else:
                    inactive_players = None
                home_team_br_id = remove_numbers(game.br_id)
                away_team_br_id = soup.select('.stats_table')[0]['id'].split('-')[1]
                
                away_team_basic = soup.select(f'#box-{away_team_br_id}-game-basic')[0]
                home_team_basic = soup.select(f'#box-{home_team_br_id}-game-basic')[0]
                
                try:
                    away_team_advanced = soup.select(f'#box-{away_team_br_id}-game-advanced')[0]
                except IndexError:
                    away_team_advanced = None

                try:
                    home_team_advanced = soup.select(f'#box-{home_team_br_id}-game-advanced')[0]
                except IndexError:
                    home_team_advanced = None

                #region GET QUARTER AND HALF STATS HTML
                if year > 1995:
                    home_team_q1 = soup.select(f'#box-{home_team_br_id}-q1-basic')[0]
                    home_team_q2 = soup.select(f'#box-{home_team_br_id}-q2-basic')[0]
                    home_team_q3 = soup.select(f'#box-{home_team_br_id}-q3-basic')[0]
                    home_team_q4 = soup.select(f'#box-{home_team_br_id}-q4-basic')[0]
                    away_team_q1 = soup.select(f'#box-{away_team_br_id}-q1-basic')[0]
                    away_team_q2 = soup.select(f'#box-{away_team_br_id}-q2-basic')[0]
                    away_team_q3 = soup.select(f'#box-{away_team_br_id}-q3-basic')[0]
                    away_team_q4 = soup.select(f'#box-{away_team_br_id}-q4-basic')[0]
                    home_team_h1 = soup.select(f'#box-{home_team_br_id}-h1-basic')[0]
                    home_team_h2 = soup.select(f'#box-{home_team_br_id}-h2-basic')[0]
                    away_team_h1 = soup.select(f'#box-{away_team_br_id}-h1-basic')[0]
                    away_team_h2 = soup.select(f'#box-{away_team_br_id}-h2-basic')[0]
                    
                else:
                    home_team_q1 = None
                    home_team_q2 = None
                    home_team_q3 = None
                    home_team_q4 = None
                    away_team_q1 = None
                    away_team_q2 = None
                    away_team_q3 = None
                    away_team_q4 = None
                    home_team_h1 = None
                    home_team_h2 = None
                    away_team_h1 = None
                    away_team_h2 = None
                #endregion
                next_field=''
                #endregion

                try:
                    
                    #region DATA SAVING
                    if get_TeamGameStats and not skip_TeamGameStats:                        
                        
                        home_tgs = {}
                        away_tgs = {}
                        
                        TeamGameStats.helper.setJSON(
                            games,
                            away_team_basic,
                            home_team_basic,
                            four_factors,
                            inactive_players,
                            away_team_advanced,
                            home_team_advanced,
                            home_tgs,
                            away_tgs,
                            file,
                            year
                        )

                        data=[away_tgs, home_tgs]

                        insertDataJL(f'TeamGameStats/json/{year}TeamGameStats.jsonl', new_data=data)
                    
                    if get_TeamGameQuarterStats and not skip_TeamGameQuarterStats:

                        home_tgs1 = {}
                        away_tgs1 = {}
                        home_tgs2 = {}
                        away_tgs2 = {}
                        home_tgs3 = {}
                        away_tgs3 = {}
                        home_tgs4 = {}
                        away_tgs4 = {}
                        
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q1,
                            home_team_q1,
                            four_factors,
                            home_tgs1,
                            away_tgs1,
                            1,
                            file,
                            year
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q2,
                            home_team_q2,
                            four_factors,
                            home_tgs2,
                            away_tgs2,
                            2,
                            file,
                            year
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q3,
                            home_team_q3,
                            four_factors,
                            home_tgs3,
                            away_tgs3,
                            3,
                            file,
                            year
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q4,
                            home_team_q4,
                            four_factors,
                            home_tgs4,
                            away_tgs4,
                            4,
                            file,
                            year
                        )

                        data=[
                            away_tgs1,
                            home_tgs1,
                            away_tgs2,
                            home_tgs2,
                            away_tgs3,
                            home_tgs3,
                            away_tgs4,
                            home_tgs4,
                        ]

                        insertDataJL(f'TeamGameQuarterStats/json/{year}TeamGameQuarterStats.jsonl', new_data=data)
                    
                    if get_TeamGameHalfStats and not skip_TeamGameHalfStats:

                        home_tgs1 = {}
                        away_tgs1 = {}
                        home_tgs2 = {}
                        away_tgs2 = {}
                        
                        TeamGameHalfStats.helper.setJSON(
                            games,
                            away_team_h1,
                            home_team_h1,
                            four_factors,
                            home_tgs1,
                            away_tgs1,
                            1,
                            file,
                            year
                        )
                        TeamGameHalfStats.helper.setJSON(
                            games,
                            away_team_h2,
                            home_team_h2,
                            four_factors,
                            home_tgs2,
                            away_tgs2,
                            2,
                            file,
                            year
                        )

                        data = [
                            away_tgs1,
                            home_tgs1,
                            away_tgs2,
                            home_tgs2,
                        ]

                        insertDataJL(f'TeamGameHalfStats/json/{year}TeamGameHalfStats.jsonl', new_data=data)
                    #endregion
                    

                        
                except Exception as e:
                    print('----------------')
                    print(f'ERROR getting {next_field}: ' + str(e) + '\n')
                    traceback.print_exc()
                    print('----------------')
                    breakpoint()
                
                    
        year -= 1



def setPlayerGameStatsJSON(
    begin_year,
    stop_year=1946,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
    testQL:str | None=None
):
    """
    :param testQL: str - SQL for one off testing rather than all games in the
        years range. Outputs to jl files with Test in the name 
    """
    begin_year = int(begin_year)
    stop_year = int(stop_year)

    year = begin_year
    
    # Get the latest game data processed. The script will have left off at the game furthest in the past
    game_leftoff_at = get_last_processed_game('PlayerGameStats')
    game_quarter_leftoff_at = get_last_processed_game('PlayerGameQuarterStats')
    game_half_leftoff_at = get_last_processed_game('PlayerGameHalfStats')
    
    while year >= stop_year:
        # DB Games
        SQL = f"""SELECT * FROM Games 
                where date_time >= '{year}-09-01'
                and date_time < '{year + 1}-09-01'
                order by date_time desc"""
                
        try:
            games = pd.read_sql(sql=SQL, con=engine)
        except Exception as e:
            print('----------------')
            print('ERROR GETTING GAME FROM DB!: ' + str(e) + '\n')
            traceback.print_exc()
            print('\nGame details:')
            print(games)
            print('----------------')
            breakpoint()
        
        new_data = []
        for file in os.listdir(f'html/{year}'):
            if file.endswith('.html'):
                
                try:
                    #region DATA PREP
                    game = games[games['br_id'] == file.split('-')[1].split('.')[0]]
                    if game.empty and testQL:
                        continue
                    game = game.iloc[0]
                    
                    if testQL:
                        # Not skipping, testing everything in the testQL query
                        skip_PlayerGameStats = False
                        skip_PlayerGameQuarterStats = False 
                        skip_PlayerGameHalfStats = False
                    else:
                        # What should we skip, if at all?
                        skip_PlayerGameStats = is_game_processed(game.br_id, game_leftoff_at)
                        skip_PlayerGameQuarterStats = is_game_processed(game.br_id, game_quarter_leftoff_at)
                        skip_PlayerGameHalfStats = is_game_processed(game.br_id, game_half_leftoff_at)
                        
                        # If data should be skipped for all specified tables, continue to the next file 
                        if (get_PlayerGameStats == False or skip_PlayerGameStats) \
                        and (get_PlayerGameQuarterStats == False or skip_PlayerGameQuarterStats) \
                        and (get_PlayerGameHalfStats == False or skip_PlayerGameHalfStats):
                            continue
                    
                    print(file)
                    
                    with open(f'html/{year}/{file}', 'r', encoding='utf-8') as f:
                        html = f.read()
                        
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    
                    four_factors = get_tag_having_text(soup, 'table', 'Four Factors Table')
                    
                    if len(soup.select('#inactive_players')) > 0:
                        inactive_players = soup.select('#inactive_players')[0]
                    
                    home_team_br_id = remove_numbers(game.br_id)
                    away_team_br_id = soup.select('.stats_table')[0]['id'].split('-')[1]
                    
                    away_team_basic = soup.select(f'#box-{away_team_br_id}-game-basic')[0]
                    home_team_basic = soup.select(f'#box-{home_team_br_id}-game-basic')[0]
                    try:
                        away_team_advanced = soup.select(f'#box-{away_team_br_id}-game-advanced')[0]
                    except IndexError:
                        away_team_advanced = None

                    try:
                        home_team_advanced = soup.select(f'#box-{home_team_br_id}-game-advanced')[0]
                    except IndexError:
                        home_team_advanced = None

                    #region GET QUARTER AND HALF STATS HTML
                    if year > 1995:

                        home_team_q1 = soup.select(f'#box-{home_team_br_id}-q1-basic')[0]
                        home_team_q2 = soup.select(f'#box-{home_team_br_id}-q2-basic')[0]
                        home_team_q3 = soup.select(f'#box-{home_team_br_id}-q3-basic')[0]
                        home_team_q4 = soup.select(f'#box-{home_team_br_id}-q4-basic')[0]
                        away_team_q1 = soup.select(f'#box-{away_team_br_id}-q1-basic')[0]
                        away_team_q2 = soup.select(f'#box-{away_team_br_id}-q2-basic')[0]
                        away_team_q3 = soup.select(f'#box-{away_team_br_id}-q3-basic')[0]
                        away_team_q4 = soup.select(f'#box-{away_team_br_id}-q4-basic')[0]
                        home_team_h1 = soup.select(f'#box-{home_team_br_id}-h1-basic')[0]
                        home_team_h2 = soup.select(f'#box-{home_team_br_id}-h2-basic')[0]
                        away_team_h1 = soup.select(f'#box-{away_team_br_id}-h1-basic')[0]
                        away_team_h2 = soup.select(f'#box-{away_team_br_id}-h2-basic')[0]
                    else:
                        home_team_q1 = None 
                        home_team_q2 = None
                        home_team_q3 = None
                        home_team_q4 = None
                        away_team_q1 = None
                        away_team_q2 = None
                        away_team_q3 = None
                        away_team_q4 = None
                        home_team_h1 = None
                        home_team_h2 = None
                        away_team_h1 = None
                        away_team_h2 = None
                    #endregion

                    next_field=''
                    #endregion
                    try:

                        #region DATA SAVING
                        if get_PlayerGameStats and not skip_PlayerGameStats:
                            home_tgs = {}
                            away_tgs = {}
                            
                            
                            new_data += PlayerGameStats.helper.setJSON(
                                game,
                                away_team_basic,
                                home_team_basic,
                                four_factors,
                                away_team_advanced,
                                home_team_advanced,
                            )
                            if testQL:
                                insertDataJL(f'PlayerGameStats/json/TestPlayerGameStats.jsonl', new_data=new_data)
                            else:
                                insertDataJL(f'PlayerGameStats/json/{year}PlayerGameStats.jsonl', new_data=new_data)
                            new_data = []
                        
                        if get_PlayerGameQuarterStats and not skip_PlayerGameQuarterStats:
                            if year > 1995:
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    1,
                                    home_team_q1,
                                    away_team_q1,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    2,
                                    home_team_q2,
                                    away_team_q2,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    3,
                                    home_team_q3,
                                    away_team_q3,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    4,
                                    home_team_q4,
                                    away_team_q4,
                                    four_factors,
                                )

                                if testQL:
                                    insertDataJL(f'PlayerGameQuarterStats/json/TestPlayerGameQuarterStats.jsonl', new_data=new_data)
                                else:
                                    insertDataJL(f'PlayerGameQuarterStats/json/{year}PlayerGameQuarterStats.jsonl', new_data=new_data)
                                new_data = []
                        
                        if get_PlayerGameHalfStats and not skip_PlayerGameHalfStats:
                            if year > 1995:
                                home_tgs1 = {}
                                away_tgs1 = {}
                                home_tgs2 = {}
                                away_tgs2 = {}
                                new_data += PlayerGameHalfStats.helper.setJSON(
                                    game,
                                    1,
                                    away_team_h1,
                                    home_team_h1,
                                    four_factors,
                                )
                                new_data += PlayerGameHalfStats.helper.setJSON(
                                    game,
                                    2,
                                    away_team_h2,
                                    home_team_h2,
                                    four_factors,
                                )

                                if testQL:
                                    insertDataJL(f'PlayerGameHalfStats/json/TestPlayerGameHalfStats.jsonl', new_data=new_data)
                                else:
                                    insertDataJL(f'PlayerGameHalfStats/json/{year}PlayerGameHalfStats.jsonl', new_data=new_data)
                                new_data = []
                        #endregion
                        
                        
                        
                            
                    except Exception as e:
                        print('\n----------------')
                        print(f'ERROR getting {next_field}: ' + str(e) + '\n')
                        traceback.print_exc()
                        print('----------------\n')
                        breakpoint()
                except Exception as e:
                    handle_err(e, game)
           
        year -= 1



def lsJSON(
                get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False, 
                get_PlayerGameStats=False,get_PlayerGameQuarterStats=False,get_PlayerGameHalfStats=False):
    '''
    Process JSON files into the database reverse chronologically
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    '''
    
    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]

    data_file_pattern = re.compile(r'\d{4}.*.jsonl')
    str_output=''
    for table in tables:
        str_output += f'\n\n{table}:'
        for file in os.listdir(f'{table}/json'):
            if data_file_pattern.match(file):
                str_output += f'\n\t{file}'

    print(str_output)


    
def rmJSON(newest_year, oldest_year,
                get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False, 
                get_PlayerGameStats=False,get_PlayerGameQuarterStats=False,get_PlayerGameHalfStats=False):
    '''
    remove JSON files from the file system
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    '''
    
    target_table_count = 0
    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]

    data_file_pattern = re.compile(r'\d{4}.*.jsonl')
    str_output=''
    for table in tables:
        str_output += f'\n\n{table}:'
        for file in os.listdir(f'{table}/json'):
            if data_file_pattern.match(file):
                if int(file[:4]) <= newest_year and int(file[:4]) >= oldest_year:
                    str_output += f'\n\tDELETED {file}'
                    
                    os.remove(f'{table}/json/{file}')

    print(str_output)
 
   

def lsdb(get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False, 
        get_PlayerGameStats=False,get_PlayerGameQuarterStats=False,get_PlayerGameHalfStats=False):
    '''
    show where progress was left off for importing data in the database 
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    '''
    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]
        
    basic_table_sql=''
    advanced_table_sql=''
    is_first_basic_table = True
    is_first_advancded_table = True
    for table in tables:
        if table.lower() in ['tgs','pgs','teamgamestats','playergamestats']:
            if is_first_basic_table:
                basic_table_sql = f'''select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}'''
            else:
                basic_table_sql += f'''\nunion select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                    union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}'''
            is_first_basic_table = False
        else:
            if is_first_advancded_table:
                advanced_table_sql = f'''select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}'''
            else:
                advanced_table_sql += f'''\nunion select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                    union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}'''
            is_first_advancded_table = False
    basic_table_sql += ';'
    with create_engine(conn_str).begin() as connection:
        basic_df = pd.read_sql(sql=basic_table_sql, con=engine)     
        advanced_df = pd.read_sql(sql=advanced_table_sql, con=engine)     
    print('\nBASIC DATA:')
    print(basic_df.to_string(index=False))
    print('\n\nADVANCED DATA:')
    print(advanced_df.to_string(index=False))
    


def loadJSONToDB(begin_year, stop_year, 
                get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False, 
                get_PlayerGameStats=False,get_PlayerGameQuarterStats=False,get_PlayerGameHalfStats=False,
                debug=False):
    '''
    Process JSON files into the database reverse chronologically
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    '''
    
    ###########################################################
    def clean_data(games):
        
        # Convert to boolean
        if 'played' in games.columns:
            games['played'] = games['played'].astype(bool)
        if 'started' in games.columns:
            games['started'] = games['started'].astype(bool)


        if get_TeamGameStats:
            games.loc[games.offensive_rebounds == '','offensive_rebounds'] = np.nan
            games.loc[games.defensive_rebounds == '','defensive_rebounds'] = np.nan
            games.loc[games.pace_factor == '','pace_factor'] = np.nan
            games.loc[games.offensive_rating == '','offensive_rating'] = np.nan
            games.loc[games.defensive_rating == '','defensive_rating'] = np.nan
            games.loc[games.offensive_rebound_percentage == '','offensive_rebound_percentage'] = np.nan
            games.loc[games.defensive_rebound_percentage == '','defensive_rebound_percentage'] = np.nan
            games.loc[games.steal_percentage == '','steal_percentage'] = np.nan
            games.loc[games.steals == '','steals'] = np.nan
            games.loc[games.turnovers == '','turnovers'] = np.nan
            games.loc[games.blocks == '','blocks'] = np.nan
            games.loc[games.field_goal_attempts == '','field_goal_attempts'] = np.nan
            games.loc[games.field_goal_percentage == '','field_goal_percentage'] = np.nan
            games.loc[games.assists == '','assists'] = np.nan
            games.loc[games.rebounds == '','rebounds'] = np.nan
            games.loc[games.personal_fouls == '','personal_fouls'] = np.nan
            games.loc[games.minutes_played == '','minutes_played'] = np.nan
            games.loc[games.ft_per_fga == '','ft_per_fga'] = np.nan
        
        if get_PlayerGameStats:
            # if '202103270LAC' in list(games.game_br_id):
            #     # TODO this is sus
            #     games.loc[(games.game_br_id == '202103270LAC') & (games.player_br_id == 'howardw01'), 'free_throw_attempt_rate'] = .609 # no idea y
            
            if '201601210DEN' in list(games.game_br_id):
                games.loc[(games.game_br_id == '201601210DEN') & (games.player_br_id == 'millemi01'), 'box_plus_minus'] = None # no idea y 
            
            if '201411070ORL' in list(games.game_br_id):
                games.loc[(games.game_br_id == '201411070ORL') & (games.player_br_id == 'bennean01'), 'box_plus_minus'] = None # no idea y 
            
            # if '201412290MIA' in list(games.game_br_id):
            #     games.loc[(games.game_br_id == '201412290MIA') & (games.player_br_id == 'whiteha01'), 'free_throw_attempt_rate'] = None # no idea y 
            
            if '201312300DEN' in list(games.game_br_id):
                games.loc[(games.game_br_id == '201312300DEN') & (games.player_br_id == 'anthojo01'), 'box_plus_minus'] = None # no idea y 
            
            if '200305250DAL' in list(games.game_br_id):
                games.loc[(games.game_br_id == '200305250DAL') & (games.player_br_id == 'kerrst01'), 'box_plus_minus'] = None # no idea y 
                
            if '200102130VAN' in list(games.game_br_id):
                games.loc[(games.game_br_id == '200102130VAN') & (games.player_br_id == 'carrch01'), 'box_plus_minus'] = None # no idea y 
                
            if '200911030DAL' in list(games.game_br_id):
                games.loc[(games.game_br_id == '200911030DAL') & (games.player_br_id == 'koufoko01'), 'box_plus_minus'] = None # no idea y 
                games.loc[(games.game_br_id == '200911030DAL') & (games.player_br_id == 'koufoko01'), 'defensive_rating'] = 0 # no idea y 
        
        
        # shift decimal two places
        def shift_decimal(val):
            if str(val) == 'nan':
                return val
            
            # weird quirk where the website shows %100 as %-1000
            if val == -1000:
                return 1.0
            
            str_val = str(val)
            dec_pos = str(str_val).rfind('.')
            if dec_pos == 0:
                return float('.00'+str_val.replace('.',''))
            elif dec_pos == 1:
                return float('.0'+str_val.replace('.',''))
            else:
                return float(str_val[:dec_pos-2]+'.'+str_val[dec_pos-2:].replace('.',''))
        
        if 'offensive_rebound_percentage' in games.columns:
            games['offensive_rebound_percentage'] = games['offensive_rebound_percentage'].apply(shift_decimal)
        if 'defensive_rebound_percentage' in games.columns:
            games['defensive_rebound_percentage'] = games['defensive_rebound_percentage'].apply(shift_decimal)
        if 'total_rebound_percentage' in games.columns:
            games['total_rebound_percentage'] = games['total_rebound_percentage'].apply(shift_decimal)
        if 'assist_percentage' in games.columns:
            games['assist_percentage'] = games['assist_percentage'].apply(shift_decimal)
        if 'steal_percentage' in games.columns:
            games['steal_percentage'] = games['steal_percentage'].apply(shift_decimal)
        if 'block_percentage' in games.columns:
            games['block_percentage'] = games['block_percentage'].apply(shift_decimal)
        if 'turnover_percentage' in games.columns:
            games['turnover_percentage'] = games['turnover_percentage'].apply(shift_decimal)
        if 'usage_percentage' in games.columns:
            games['usage_percentage'] = games['usage_percentage'].apply(shift_decimal)
        if 'box_plus_minus' in games.columns:
            games['box_plus_minus'] = games['box_plus_minus'].apply(lambda x: None if x == -1000 else x)
        

        if 'three_pointer_percentage' in games.columns:
            
            games.three_pointer_percentage = games.three_pointer_percentage.apply(lambda val : 0 if val == '.000' else val)
            games.three_pointer_percentage = games.three_pointer_percentage.apply(lambda val : np.nan if val == '' else val)

            games.free_throw_percentage = games.free_throw_percentage.apply(lambda val : 0 if val == '.000' else val)
            games.free_throw_percentage = games.free_throw_percentage.apply(lambda val : np.nan if val == '' else val)
        if 'inactive_players' in games.columns:
            games["inactive_players"] = games["inactive_players"].apply(lambda x: json.dumps(x))
        if 'minutes_played' in games.columns and (get_PlayerGameStats or get_PlayerGameQuarterStats or get_PlayerGameHalfStats):
            games['seconds_played'] = games['minutes_played'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if not x in [None, 'DNP'] else None)
            del games['minutes_played']
        
                
        return games
    ###########################################################
    
    target_table_count = 0
    if get_TeamGameStats:
        TABLE_NAME = "TeamGameStats"
        target_table_count += 1
    if get_TeamGameQuarterStats:
        TABLE_NAME = "TeamGameQuarterStats"
        target_table_count += 1
    if get_TeamGameHalfStats:
        TABLE_NAME = "TeamGameHalfStats"
        target_table_count += 1
    if get_PlayerGameStats:
        TABLE_NAME = "PlayerGameStats"
        target_table_count += 1
    if get_PlayerGameQuarterStats:
        TABLE_NAME = "PlayerGameQuarterStats"
        target_table_count += 1
    if get_PlayerGameHalfStats:
        TABLE_NAME = "PlayerGameHalfStats"
        target_table_count += 1

    # Backup table in use
    if debug:
        TABLE_NAME += "2"

    if target_table_count > 1:
        print("Only one table can be loaded at a time")
        exit(1)

    games = None
    try:
        
        begin_year = int(begin_year)
        stop_year = int(stop_year)
        year = begin_year
        games_paginated = None
        while year >= stop_year:
            with create_engine(conn_str).begin() as connection:
                connection.execute(text('SET FOREIGN_KEY_CHECKS=0;'))
            
                with open(f'{TABLE_NAME}/json/{year}{TABLE_NAME}.jsonl', 'r') as f:
                    games = pd.read_json(f,lines=True)
                
                games = clean_data(games)
                page = 1
                chunksize = 1000 #!
                while page * chunksize < len(games):
                    try:
                        games_paginated = games.iloc[(page - 1) * chunksize : page * chunksize]
                        games_paginated.to_sql(
                            name=TABLE_NAME,
                            con=connection,
                            if_exists="append",
                            chunksize=chunksize,
                            index=False,
                        )
                        with open("log.txt", "w") as f:
                            f.write(str(page))
                        page += 1
                    except Exception as e:
                        with open("log.txt", "a+") as f:
                            f.write(str(e))
                        break

                games.iloc[(page - 1) * chunksize :].to_sql(
                    name=TABLE_NAME, con=connection, if_exists="append", chunksize=chunksize, index=False
                )
                year -= 1
                
                connection.execute(text('SET FOREIGN_KEY_CHECKS=1;'))                
    except Exception as e:
        handle_err(e, games_paginated=games_paginated)
        breakpoint()



def rmdb(oldest_year: int, newest_year: int, 
        get_TeamGameStats=False,get_TeamGameQuarterStats=False,get_TeamGameHalfStats=False, 
        get_PlayerGameStats=False,get_PlayerGameQuarterStats=False,get_PlayerGameHalfStats=False):

    target_table_count = 0
    if get_TeamGameStats:
        TABLE_NAME = "TeamGameStats"
        target_table_count += 1
    if get_TeamGameQuarterStats:
        TABLE_NAME = "TeamGameQuarterStats"
        target_table_count += 1
    if get_TeamGameHalfStats:
        TABLE_NAME = "TeamGameHalfStats"
        target_table_count += 1
    if get_PlayerGameStats:
        TABLE_NAME = "PlayerGameStats"
        target_table_count += 1
    if get_PlayerGameQuarterStats:
        TABLE_NAME = "PlayerGameQuarterStats"
        target_table_count += 1
    if get_PlayerGameHalfStats:
        TABLE_NAME = "PlayerGameHalfStats"
        target_table_count += 1
        
    if target_table_count > 1:
        print("Only one table can be loaded at a time")
        exit(1)
    
    with engine.begin() as connection:        
        # Games for each year start no earlier than september, so all games
        # between {oldest_year}0901 (Sept. 1) and {newest_year + 1}0901 are
        # deleted
        SQL=f"""
            DELETE FROM {TABLE_NAME}
            WHERE game_br_id > '{oldest_year}0901'
            AND game_br_id <= '{newest_year + 1}0901'
            """
        print(SQL)
        result = connection.execute(text(SQL))
        print(f"Rows deleted: {result.rowcount}")
    
    

if __name__ == '__main__':
    if args.seasons_range:
        if '-' in args.seasons_range:
            year1, year2 = args.seasons_range.split('-')
            if year1 < year2:
                oldest_year = int(year1)
                newest_year = int(year2)
            else:
                oldest_year = int(year2)
                newest_year = int(year1)
        else:
            newest_year=int(args.seasons_range)
            oldest_year=1946
    
    match args.format:
        case 'json':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats=True
            if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats=True
            if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats=True
            if 'playergamestats' in args.tables or 'pgs' in args.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats=True
            if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats=True
            if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats=True
            

            if get_TeamGameStats or get_TeamGameQuarterStats or get_TeamGameHalfStats:
                setTeamGameStatsJSON(
                    newest_year,
                    oldest_year,
                    get_TeamGameStats=get_TeamGameStats,
                    get_TeamGameHalfStats=get_TeamGameHalfStats,
                    get_TeamGameQuarterStats=get_TeamGameQuarterStats)
            if get_PlayerGameStats or get_PlayerGameQuarterStats or get_PlayerGameHalfStats:
                setPlayerGameStatsJSON(
                    newest_year,
                    oldest_year,
                    get_PlayerGameStats=get_PlayerGameStats,
                    get_PlayerGameHalfStats=get_PlayerGameHalfStats,
                    get_PlayerGameQuarterStats=get_PlayerGameQuarterStats)
            
            exit(0)

        case 'lsjson':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            if args.tables:
                if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                    get_TeamGameStats=True
                if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                    get_TeamGameQuarterStats=True
                if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                    get_TeamGameHalfStats=True
                if 'playergamestats' in args.tables or 'pgs' in args.tables:
                    get_PlayerGameStats=True
                if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                    get_PlayerGameQuarterStats=True
                if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            lsJSON(get_TeamGameStats, get_TeamGameQuarterStats, get_TeamGameHalfStats, get_PlayerGameStats, get_PlayerGameQuarterStats, get_PlayerGameHalfStats)
            
        case 'rmjson':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            if args.tables:
                if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                    get_TeamGameStats=True
                if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                    get_TeamGameQuarterStats=True
                if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                    get_TeamGameHalfStats=True
                if 'playergamestats' in args.tables or 'pgs' in args.tables:
                    get_PlayerGameStats=True
                if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                    get_PlayerGameQuarterStats=True
                if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            
            rmJSON(newest_year,
                    oldest_year,
                    get_TeamGameStats,
                    get_TeamGameQuarterStats,
                    get_TeamGameHalfStats,
                    get_PlayerGameStats,
                    get_PlayerGameQuarterStats,
                    get_PlayerGameHalfStats)
        
        case 'lsdb':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            if args.tables:
                if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                    get_TeamGameStats=True
                if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                    get_TeamGameQuarterStats=True
                if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                    get_TeamGameHalfStats=True
                if 'playergamestats' in args.tables or 'pgs' in args.tables:
                    get_PlayerGameStats=True
                if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                    get_PlayerGameQuarterStats=True
                if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            lsdb(get_TeamGameStats, get_TeamGameQuarterStats, get_TeamGameHalfStats, get_PlayerGameStats, get_PlayerGameQuarterStats, get_PlayerGameHalfStats)
        
        case 'db':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            tables = args.tables.split(',')
            if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats=True
            if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats=True
            if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats=True
            if 'playergamestats' in args.tables or 'pgs' in args.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats=True
            if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats=True
            if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats=True
                

            loadJSONToDB(
                newest_year, 
                oldest_year, 
                get_TeamGameStats=get_TeamGameStats,
                get_TeamGameHalfStats=get_TeamGameHalfStats,
                get_TeamGameQuarterStats=get_TeamGameQuarterStats,
                get_PlayerGameStats=get_PlayerGameStats,
                get_PlayerGameHalfStats=get_PlayerGameHalfStats,
                get_PlayerGameQuarterStats=get_PlayerGameQuarterStats,
            )
            
            exit(0)

        case 'rmdb':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            if args.tables:
                if 'teamgamestats' in args.tables or 'tgs' in args.tables:
                    get_TeamGameStats=True
                if 'teamgamequarterstats' in args.tables or 'tgqs' in args.tables:
                    get_TeamGameQuarterStats=True
                if 'teamgamehalfstats' in args.tables or 'tghs' in args.tables:
                    get_TeamGameHalfStats=True
                if 'playergamestats' in args.tables or 'pgs' in args.tables:
                    get_PlayerGameStats=True
                if 'playergamequarterstats' in args.tables or 'pgqs' in args.tables:
                    get_PlayerGameQuarterStats=True
                if 'playergamehalfstats' in args.tables or 'pghs' in args.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            rmdb(
                oldest_year, newest_year,
                get_TeamGameStats, get_TeamGameQuarterStats,
                get_TeamGameHalfStats, get_PlayerGameStats,
                get_PlayerGameQuarterStats, get_PlayerGameHalfStats
            )
            # lsdb(get_TeamGameStats, get_TeamGameQuarterStats, get_TeamGameHalfStats, get_PlayerGameStats, get_PlayerGameQuarterStats, get_PlayerGameHalfStats)
        
        case 'html':
            getTeamGameStatsHTML(newest_year, oldest_year, override_existing_html=False) 
            exit(0)

