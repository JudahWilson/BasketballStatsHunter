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
import re
import argparse
import warnings
from sqlalchemy import text
# from sqlalchemy.exc import RemovedIn20Warning
warnings.filterwarnings("ignore", category=UserWarning)
# warnings.filterwarnings("ignore", category=RemovedIn20Warning)
import pyperclip
import duckdb
from core.core import getTeamGameStatsHTML, setTeamGameStatsJSON, setPlayerGameStatsJSON, lsJSON, rmJSON, lsdb, loadJSONToDB, rmdb
from pydantic import BaseModel
import json
from typing import Literal
#endregion


    
class Controls(BaseModel):
    """Important variables that tell the script what to do"""
    format: Literal['json', 'db', 'html','rmjson','lsjson','lsdb','rmdb']
    oldest_year: int | None = None
    newest_year: int | None = None 
    tables: list[Literal[
            'teamgamestats', 'tgs',
            'teamgamequarterstats', 'tgqs', 
            'teamgamehalfstats', 'tghs',
            'playergamestats', 'pgs',
            'playergamequarterstats', 'pgqs',
            'playergamehalfstats', 'pghs'
    ]] | None = None

    def model_post_init(self, *args, **kwargs):
        
        if self.format in ['json','db','rmjson'] and not self.tables:
            raise ValueError(f'table option is required for {self.format}')
            
        if self.format not in ['lsjson','lsdb'] and not self.newest_year:
            raise ValueError(f'seasons_range is required for {self.format}')
    

def get_controls_from_cli_args(args: argparse.Namespace) -> Controls:
    
    if args.seasons_range:
        if not re.match(r'^\d{4}$', args.seasons_range) and not re.match(r'^\d{4}-\d{4}$', args.seasons_range):
            parser.error('Invalid seasons range. Must be in the format YYYY-YYYY (both years are the starting year of their season)')
                
    oldest_year=None
    newest_year=None
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
                
    return Controls(
        format=args.format,
        oldest_year=oldest_year,
        newest_year=newest_year,
        tables=args.tables.split(',') if args.tables else None
    )
    
    
def get_controls_from_file():
    with open('controls.json', 'r') as f:
        controls = json.load(f)
    return Controls(**controls)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'format', 
        help='json, html, db, rmjson (to remove json files that you are finished with)', 
        choices=['json', 'db', 'html','rmjson','lsjson','lsdb','rmdb'],
        nargs='?',
    )
    parser.add_argument(
        'seasons_range', 
        type=str, 
        nargs='?',
        help='Oldest season\'s start year to the most recent season\'s start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]'
    )
    parser.add_argument(
        'tables', 
        help=''''
            [CSV] teamgamestats' ('tgs')
            'teamgamequarterstats' ('tgqs')
            'teamgamehalfstats' ('tghs')
            'playergamestats' ('pgs')
            'playergamequarterstats' ('pgqs')
            'playergamehalfstats' ('pghs')''',
        nargs='?'
    )
    parser.add_argument(
        '--file', 
        action='store_true',
        help='Gather all program controls from controls.json instead of CLI args'
    )

    args = parser.parse_args()
    if args.file:
        controls = get_controls_from_file()
    else:
        if not args.format:
            if input('No format provided. Do you want to use controls.json? (y)') in ('y',''):
                controls = get_controls_from_file()
            else:    
                raise Exception('No format provided. Exiting...')
        else:
            controls = get_controls_from_cli_args(args)
    
    match controls.format:
        case 'json':
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            
            if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats=True
            
            if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats=True
            
            if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats=True
            
            if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats=True
            
            if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats=True
            
            if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats=True
            

            if get_TeamGameStats or get_TeamGameQuarterStats or get_TeamGameHalfStats:
                setTeamGameStatsJSON(
                    controls.newest_year,
                    controls.oldest_year,
                    get_TeamGameStats=get_TeamGameStats,
                    get_TeamGameHalfStats=get_TeamGameHalfStats,
                    get_TeamGameQuarterStats=get_TeamGameQuarterStats)
            if get_PlayerGameStats or get_PlayerGameQuarterStats or get_PlayerGameHalfStats:
                setPlayerGameStatsJSON(
                    controls.newest_year,
                    controls.oldest_year,
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
            
            if controls.tables:
                
                if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                    get_TeamGameStats=True
                
                if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                    get_TeamGameQuarterStats=True
                
                if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                    get_TeamGameHalfStats=True
                
                if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                    get_PlayerGameStats=True
                
                if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                    get_PlayerGameQuarterStats=True
                
                if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
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
            
            if controls.tables:
                
                if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                    get_TeamGameStats=True
                
                if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                    get_TeamGameQuarterStats=True
                
                if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                    get_TeamGameHalfStats=True
                
                if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                    get_PlayerGameStats=True
                
                if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                    get_PlayerGameQuarterStats=True
                
                if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            
            rmJSON(controls.newest_year,
                    controls.oldest_year,
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
            
            if controls.tables:
                
                if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                    get_TeamGameStats=True
                
                if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                    get_TeamGameQuarterStats=True
                
                if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                    get_TeamGameHalfStats=True
                
                if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                    get_PlayerGameStats=True
                
                if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                    get_PlayerGameQuarterStats=True
                
                if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
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
            
            tables = controls.tables
            
            if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats=True
            
            if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats=True
            
            if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats=True
            
            if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats=True
            
            if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats=True
            
            if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats=True
                

            loadJSONToDB(
                controls.newest_year, 
                controls.oldest_year, 
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
            
            if controls.tables:
                
                if 'teamgamestats' in controls.tables or 'tgs' in controls.tables:
                    get_TeamGameStats=True
                
                if 'teamgamequarterstats' in controls.tables or 'tgqs' in controls.tables:
                    get_TeamGameQuarterStats=True
                
                if 'teamgamehalfstats' in controls.tables or 'tghs' in controls.tables:
                    get_TeamGameHalfStats=True
                
                if 'playergamestats' in controls.tables or 'pgs' in controls.tables:
                    get_PlayerGameStats=True
                
                if 'playergamequarterstats' in controls.tables or 'pgqs' in controls.tables:
                    get_PlayerGameQuarterStats=True
                
                if 'playergamehalfstats' in controls.tables or 'pghs' in controls.tables:
                    get_PlayerGameHalfStats=True
            else:
                get_TeamGameStats=True
                get_TeamGameQuarterStats=True
                get_TeamGameHalfStats=True
                get_PlayerGameStats=True
                get_PlayerGameQuarterStats=True
                get_PlayerGameHalfStats=True
            rmdb(
                controls.oldest_year, controls.newest_year,
                get_TeamGameStats, get_TeamGameQuarterStats,
                get_TeamGameHalfStats, get_PlayerGameStats,
                get_PlayerGameQuarterStats, get_PlayerGameHalfStats
            )
            # lsdb(get_TeamGameStats, get_TeamGameQuarterStats, get_TeamGameHalfStats, get_PlayerGameStats, get_PlayerGameQuarterStats, get_PlayerGameHalfStats)
        
        case 'html':
            getTeamGameStatsHTML(controls.newest_year, controls.oldest_year, override_existing_html=False) 
            exit(0)

