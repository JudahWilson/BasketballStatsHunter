import pandas as pd
import json
from json import JSONEncoder
import bs4
import os, re
import time
import traceback
import pyperclip
import requests
import jsonlines
import glob
from dotenv import load_dotenv
from sqlalchemy import create_engine
import numpy as np

WEBSCRAPE_DEBOUNCER = 4 # seconds to wait between web requests

load_dotenv()
conn_str = f"mysql+mysqlconnector://{os.environ['BACKEND_DB_USER']}:{os.environ['BACKEND_DB_PASSWORD']}@{os.environ['BACKEND_DB_HOST']}/{os.environ['BACKEND_DB_NAME']}"
engine = create_engine(conn_str)

# The website's base url
base_url = 'https://www.basketball-reference.com'


def get_soup(url):
    """
    Get a BeautifulSoup object from a url

    Args:
        url (str): the url to get the soup from

    Raises:
        Exception: A failure to get the data from the url

    Returns:
        BeautifulSoup: the soup object
    """
    print(url)
    response = requests.get(url)
    time.sleep(WEBSCRAPE_DEBOUNCER)
    if response.status_code < 200 or response.status_code > 299:
        time.sleep(10)
        print('RETRY')
        response = requests.get(url)
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f'Error getting data from {url}. Status ' + str(response.status_code))

    return bs4.BeautifulSoup(response.text, 'html.parser')


def get_tag_having_text(soup, selector, needle) -> bs4.element.Tag | None:
    """
    get a tag from a selector that has the provided text in it
    """
    tags = soup.find_all(selector)
    for tag in tags:
        if needle in tag.text:
            return tag
        
    return None


def handle_err(e, game=None, games_paginated=None, additional_message=None):
    #########################################
    # TODO, options to show json? html file path? maybe the traceback and traceback is default to not be shown?
    #########################################
    
    
    print('----------------')
    print('ERROR: ' + str(e) + '\n')
    traceback.print_exc()
    
    # If the game data is not specified, but we may can get the game from the
    # page of game data
    if game is None:
        
        if isinstance(games_paginated, pd.DataFrame) and not games_paginated.empty:
            
            # If a row is specified in a page of rows
            if ' at row ' in e.args[0]:
            
                # If we can pull the row number successfully
                match = re.match(r'.* at row (\d+).*', e.args[0])
                if match:
                    index = int(match.group(1)) - 1
                    game = games_paginated.iloc[index]
                        
    if game is not None:
        print('\nGame details:')
        print(game)
    
    if additional_message:
        print(additional_message)
    
    breakpoint()
    print('----------------')


class CustomEncoder(JSONEncoder):
     def default(self, obj):
         if isinstance(obj, np.int64):
             return int(obj)
         return super().default(obj)


def remove_numbers(input_string: str):
    return re.sub(r'\d+', '', input_string)


def save_html(game, year):
    print(game['br_id'])

    try:
        url = base_url + "/boxscores/" + game['br_id'] + ".html"
    except Exception as e:
        breakpoint()
        breakpoint()
    soup = get_soup(url)
    
    html = ''
    
    # four factors table
    if four_factors:=re.findall(r'<table[^>]*id="four_factors"[^>]*>(.*?)</table>', str(soup), re.DOTALL):
        html += '<table>' + four_factors[0] + '</table>'
    else:
        with open("log.txt", "a+") as f:
            f.write('\nNo four factors table found for game ' + game['br_id'] + '\n')
    
    # inactive players
    inactive_strong_tag = soup.find('strong', string=re.compile(r'Inactive:', re.IGNORECASE))
    if inactive_strong_tag:
        html += '<div id="inactive_players">'+str(inactive_strong_tag.find_parent('div'))+'</div>'
    else:
        with open("log.txt", "a+") as f:
            f.write('\nNo inactive players found for game ' + game['br_id'] + '\n')
    
    
    # Away Team basic
    try:
        html += soup.select(f"#box-{game['away_team_br_id']}-game-basic")[0].prettify() + '\n'
    except Exception as e:
        handle_err(e, game)                
        
    
    # away team advanced
    try:
        html += soup.select(f"#box-{game['away_team_br_id']}-game-advanced")[0].prettify() + '\n'
    except IndexError:
        pass
    except Exception as e:
        handle_err(e, game)                
        
    
    # Home Team basic
    try:
        html += soup.select(f"#box-{game['home_team_br_id']}-game-basic")[0].prettify() + '\n'
    except Exception as e:
        handle_err(e, game)               
    
    
    # home team advanced
    try:
        html += soup.select(f"#box-{game['home_team_br_id']}-game-advanced")[0].prettify() + '\n'
    except IndexError:
        pass
    except Exception as e:
        handle_err(e, game)                
    
    if year > 1995:
        # home team q1
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-q1-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)               
        
        # home team q2
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-q2-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # home team q3
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-q3-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
    
        # home team q4
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-q4-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # away team q1
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-q1-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # away team q2
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-q2-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # away team q3
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-q3-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
    
        # away team q4
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-q4-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # home h1
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-h1-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # home h2
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-h2-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # away h1
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-h1-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)                
            
        
        # away h2
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-h2-basic")[0].prettify() + '\n'
        except Exception as e:
            handle_err(e, game)       
            
        # home ot1
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot1-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # away ot1
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot1-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # home ot2
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot2-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # away ot2
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot2-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # away homet3
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot3-basic")[0].prettify() + '\n'
        except Exception as e:
            pass        
        
        # away ot3
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot3-basic")[0].prettify() + '\n'
        except Exception as e:
            pass        
        
        # away homet4
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot4-basic")[0].prettify() + '\n'
        except Exception as e:
            pass    
        
        # away ot4
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot4-basic")[0].prettify() + '\n'
        except Exception as e:
            pass    
        
        # home ot5
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot5-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # away ot5
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot5-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # home ot6
        try:
            html += soup.select(f"#box-{game['home_team_br_id']}-ot6-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
        # away ot6
        try:
            html += soup.select(f"#box-{game['away_team_br_id']}-ot6-basic")[0].prettify() + '\n'
        except Exception as e:
            pass
        
    # If the year folder isn't there, create it
    if not os.path.exists(f'html/{year}'):
        os.makedirs(f'html/{year}')
    
    with open(f'html/{year}/TeamGameStats-{game["br_id"]}.html', 'w', encoding='utf-8') as f:
        f.write(html)


def insertData(fname, new_data):
    # Get data currently in file
    try:
        f = open(fname, 'r')
        data = json.load(f)
    except FileNotFoundError:
        f = open(fname, 'w')
        f.write('[]')
        data = []
    finally:
        f.close()
    f.close()
    
    # write the new data and current data into the file
    with open(fname, 'w', encoding='utf-8') as f:
        data += new_data
        json.dump(data, f, cls=CustomEncoder)


def insertDataJL(fname, new_data):
    '''
    Insert data into a jsonlines file
    '''
    new_data = [{k: int(v) if isinstance(v, np.int64) else v for k, v in item.items()} for item in new_data]

    if os.path.exists(fname):
        with jsonlines.open(fname, 'a') as writer:
            writer.write_all(new_data)
    else:
        with jsonlines.open(fname, 'w') as writer:
            writer.write_all(new_data)


def get_last_processed_game(table_name: str) -> str | None:
    # Get json lines files in descending chronological order
    files = glob.glob(f'{table_name}/json/*.jsonl')
    files.sort(reverse=True)
    
    # Get the last season processed (chronologically the earliest)
    season_year_leftoff = 9999
    for file in files:
        season_year = int(re.findall(r'\d+', file.split('/')[-1].split('.')[0])[0])
        if season_year < season_year_leftoff:
            season_year_leftoff = season_year
    
    #! If no season has been processed, return None
    if season_year_leftoff == 9999:
        return None

    # Get the last game processed in the season (chronolgically the latest of that season)
    leftoff_filename = f'{table_name}/json/{season_year_leftoff}{table_name}.jsonl'
    try:
        x = pd.read_json(leftoff_filename, lines=True)
        if not x.empty:
            # The last game processed is the one played at the latest date of the season thus far 
            temp = x['game_br_id'].tolist()
            temp.sort()
            game_leftoff_at = temp[-1]
            
    except Exception as e:
        handle_err(e, additional_message='ERROR DETERMINING THE LAST GAME PROCESSED (to pick up were the script left off)!')    

    return game_leftoff_at


def get_season_from_br_id(br_id: str) -> int:
    """
    Get the season from the br_id. It is the year of the season if the month is
    October, November, or December. Otherwise, it is the year of the season - 1.

    Args:
        br_id (str): Game BR ID (e.g. 2023100001)

    Returns:
        int: start year of the game's season season (e.g. 2023)
    """
    year = br_id[:4]
    month = br_id[4:6]
    if month in ['10', '11', '12']:
        return int(year)
    else:
        return int(year) - 1
    

def is_game_processed(game_in_question: str, game_leftoff_at: str) -> bool:
    '''
    Has the game in question been processed already?
    
    Considering that seasons are processed reverse chronological order and games
    per season are processed in chronological order, has the game in question 
    been processed.
    '''
    if game_leftoff_at is None:
        return False
    
    season_in_question = get_season_from_br_id(game_in_question)
    season_leftoff_at = get_season_from_br_id(game_leftoff_at)

    if season_in_question > season_leftoff_at:
        return True
    elif season_in_question == season_leftoff_at:
        if game_in_question <= game_leftoff_at:
            return True
        else:
            return False
    else: 
        return False

