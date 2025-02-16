import pandas as pd
import duckdb
from pbp_helper import *
import argparse
from PlayByPlays.process_html import process_html

# region ARGS
parser = argparse.ArgumentParser()
parser.add_argument('format', help='json, html, db, rmjson (to remove json files that you are finished with)', choices=['json', 'db', 'html','rmjson','lsjson','lsdb'])
parser.add_argument('seasons_range', type=str, nargs='?',
                    help='Oldest season\'s start year to the most recent season\'s start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]')

args = parser.parse_args()
if args.seasons_range:
    if not re.match(r'^\d{4}$', args.seasons_range) and not re.match(r'^\d{4}-\d{4}$', args.seasons_range):
        parser.error('Invalid seasons range. Must be in the format YYYY-YYYY (both years are the starting year of their season)')

if args.format not in ['lsjson','lsdb'] and not args.seasons_range:
    parser.error(f'seasons_range is required for {args.format} (YYYY-YYYY) or just YYYY for all seasons YYYY and earlier')
#endregion


    
    
def getPlayByPlaysHTML(start_year=None, stop_year=1946):
    
    start_year = int(start_year)
    stop_year = int(stop_year)

    year = start_year
    while year >= stop_year:
        SQL = f"""SELECT * FROM Games 
        where date_time >= '{year}-09-01'
        and date_time < '{year + 1}-09-01'
        order by date_time desc"""
        
        games = pd.read_sql(sql=SQL, con=engine)
        
        # TODO Catch up to where we left off
        left_off_game_br_id = None
        
                
        for ind, game in games.iterrows():
            # TODO
            # if left_off_game_br_id:
            #     # Pick up where we left off if we have to
            #     if left_off_game_br_id == game['br_id']:
            #         # Skip to the next game
            #         if left_off_game_br_id:
            #             left_off_game_br_id = False
            #     continue
            
            print(game['br_id'])

            try:
                url = base_url + "/boxscores/pbp/" + game['br_id'] + ".html"
            except Exception as e:
                breakpoint()
            
            soup = get_soup(url)
            
            try:
                html = str(soup.select('#pbp')[0])
                
                # If the year folder isn't there, create it
                if not os.path.exists(f'html/{year}'):
                    os.makedirs(f'html/{year}')
                
                with open(get_pbp_filename(game['br_id']), 'w', encoding='utf-8') as f:
                    f.write(html)
                    
            except Exception as e:
                breakpoint()
            
            print('SAVED')
        print('YEAR ' + str(year) + ' COMPLETE')
        year -= 1
    print('EXITED')


def getPlayByPlaysJSON(start_year=None, stop_year=1946):
    # TODO
    raise NotImplementedError('No code written for this getPlayByPlaysJSON')


def loadHTMLToDB(newest_year,oldest_year):
    # TODO
    raise NotImplementedError('No code written for this loadHTMLToDB')


def lsdb():
    # TODO 
    raise NotImplementedError('No code written for this lsdb')

    
if __name__ == '__main__':
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
  
    
    if args.format == 'html':
        getPlayByPlaysHTML(newest_year, oldest_year) 
        exit(0)

    elif args.format == 'db':
        loadHTMLToDB(newest_year,oldest_year)
        exit(0)