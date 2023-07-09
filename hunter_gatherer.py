"""
if a function 
    starts with 'download' it will download the data from the internet
    starts with 'store' it will store the data into the database
    ends with a number, it is one of several functions doing the downloading or storing
"""

import json
from project import *
import pandas as pd
import bs4
import re
import time
from nameparser import HumanName
##########################################
# TEAMS
##########################################
def download_teams1():
    """
    Download the teams from basketball-reference.com
    """
    url = 'https://www.basketball-reference.com/teams/'
    soup = get_soup(url)
    teams_html = soup.find_all('tr', {'class':'full_table'})
    with open('html/teams.html', 'w') as f:
        f.write('\n'.join([str(t) for t in teams_html]))

def store_teams():
    """
    Load the teams from the teams.csv file into the database
    """
    teams = pd.read_csv(r'unprocessed data\teams\teams.csv')
    processed_data = pd.DataFrame()
    processed_data['location'] = teams['location']
    processed_data['name'] = teams['name']
    processed_data['nba'] = teams['Lg'].apply(lambda x: True if 'NBA' in x else False)
    processed_data['aba'] = teams['Lg'].apply(lambda x: True if 'ABA' in x else False)
    processed_data['baa'] = teams['Lg'].apply(lambda x: True if 'BAA' in x else False)
    processed_data['season_start'] = teams['From'].apply(lambda x: x.split('-')[0])
    processed_data['season_end'] = teams['To'].apply(lambda x: 
        (x[0:2] if x.split('-')[1] != '00' else '20') + x.split('-')[1]
    )
    
    processed_data.to_sql('teams', db.conn, if_exists='append', index=False)

##########################################
# SEASONS
##########################################
def load_seasons():
    with open('workhorse/unprocessed data/seasons/seasons.html' , 'r', encoding='utf-8') as f:
        s = f.read()
        soup = bs4.BeautifulSoup(s)
    
    html_rows = soup.select('tbody>tr:not(.thead)')
    
    db_rows = []
    for html_row in html_rows:
        db_row = {}
        cells = html_row.find_all(['th','td'])

        # year
        db_row['season_start'] = int(cells[0].text.strip().split('-')[0])
        if db_row['season_start'] >= 2000:
            db_row['season_end'] = 2000 + int(cells[0].text.strip().split('-')[1])
        else: 
            db_row['season_end'] = 1900 + int(cells[0].text.strip().split('-')[1])

        # Leauge
        db_row['league'] = re.search('/leagues/([A-Z]{3})_\d{4}.html',cells[1].a['href'])[1]
        
        # basketball reference ID
        db_row['br_id'] = cells[0].find('a')['href'].split('/')[-1].replace('.html','')   
        
        # Champion
        if cells[2].find('a'):
            db_row['champion_br_id'] = cells[2].find('a')['href'].split('/')[-2]
        else:
            db_row['champion_br_id'] = None
            
        # MVP
        if cells[3].find('a'):
            db_row['mvp_br_id'] = cells[3].find('a')['href'].split('/')[-1].replace('.html','')
        else:
            db_row['mvp_br_id'] = None
            
        # ROY
        if cells[4].find('a'):
            db_row['roy_br_id'] = cells[4].find('a')['href'].split('/')[-1].replace('.html','')
        else:
            db_row['roy_br_id'] = None

        # Scoring leader
        if cells[5].find('a'):
            db_row['scoring_leader_br_id'] = cells[5].find('a')['href'].split('/')[-1].replace('.html','')
            # Scoring leader points
            db_row['scoring_leader_points'] = re.findall(r'\((\d+(?:\.\d+)?)\)', cells[5].text)[0]
        else:
            db_row['scoring_leader_br_id'] = None
            db_row['scoring_leader_points'] = None
            
        
        # Rebounding leader
        if cells[6].find('a'):
            db_row['rebounding_leader_br_id'] = cells[6].find('a')['href'].split('/')[-1].replace('.html','')
        else:
            db_row['rebounding_leader_br_id'] = None
            
        # Assists leader
        if cells[7].find('a'):
            db_row['assists_leader_br_id'] = cells[7].find('a')['href'].split('/')[-1].replace('.html','')
        else:
            db_row['assists_leader_br_id'] = None

        # Win Shares leader
        if cells[8].find('a'):
            db_row['winshares_leader_br_id'] = cells[8].find('a')['href'].split('/')[-1].replace('.html','')
        else:
            db_row['winshares_leader_br_id'] = None
        
        db_rows.append(db_row)
        
    # store the db_rows into seasons table that already exists
    seasons_df = pd.DataFrame(db_rows).rename(columns={
        '':''}
    )
    
    seasons_df.to_sql('seasons', db.conn, if_exists='append', index=False)


##########################################     
# PLAYERS
##########################################     
def download_players1():
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','y','z']
    # for each letter
    db_rows = []
    for letter in letters:
        player_list_soup = get_soup(base_url + '/players/' + letter)
        players_rows = player_list_soup.select('tbody > tr:not(.thead)')
        # for each player
        for row in players_rows:
            db_row = {}
            cells = row.find_all(['th','td'])
            db_row['br_id'] = cells[0].find('a')['href'].split('/')[-1].replace('.html','')
            name = HumanName(cells[0].text.strip())
            db_row['full_name'] = name.full_name
            db_row['first_name'] = name.first
            db_row['last_name'] = name.last.replace('*','')
            db_row['suffix'] = name.suffix.replace('*','')
            db_row['year_start'] = cells[1].text.strip()
            db_row['year_end'] = cells[2].text.strip()
            db_row['position'] = cells[3].text.strip().replace('-','')
            db_row['height_str'] = cells[4].text.strip()
            db_row['height_in'] = cells[4]['csk']
            db_row['weight'] = cells[5].text.strip()
            if 'csk' in cells[6].attrs:
                x = cells[6]['csk']
                db_row['birth_date'] = x[:4] + '-' + x[4:6] + '-' + x[6:]
            db_row['colleges'] = json.dumps([x.text.strip() for x in cells[7].find_all('a')])
            db_rows.append(db_row)
    pd.DataFrame(db_rows).to_csv('workhorse\\unprocessed data\\players\\players.csv',index=False)
            
def load_players1():
    x=pd.read_excel(r'C:\Users\Judah Wilson\My Drive\Programming\Basketball Stats\workhorse\unprocessed data\players\players.xlsx')   
    
#########################################
# Play by play 
#########################################
def download_and_store_play_by_play(start_date=None):
    """Mother of all data, this downloads the game data and play data for every
    game, one at a time given a start date
    """
    
    # Need logic to intelligently decide when to stop looking at days for games
    # (2 weeks without games maybe?)
    
    # example url showing games per day
    #https://www.basketball-reference.com/boxscores/?month=11&day=21&year=1971
    
    # at certain point, play by play is included (somewhere in the 90s)