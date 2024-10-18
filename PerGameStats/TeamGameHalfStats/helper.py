import pandas as pd
import pyperclip
from io import StringIO

def setJSON(games, away_team_basic, home_team_basic, four_factors, home_tgs, away_tgs, half, file, year, accidently_set_team_br_id_backwards=True):
    """
    Set the JSON object for the TeamGameStats object.

    Parameters
    ----------
    games : DataFrame
        DataFrame containing the games data.
    away_team_basic : BeautifulSoup
        BeautifulSoup object containing the away team basic stats.
    home_team_basic : BeautifulSoup
        BeautifulSoup object containing the home team basic stats.
    four_factors : BeautifulSoup
        BeautifulSoup object containing the four factors stats.
    inactive_players : BeautifulSoup
        BeautifulSoup object containing the inactive players.
    away_team_advanced : BeautifulSoup
        BeautifulSoup object containing the away team advanced stats.
    home_team_advanced : BeautifulSoup
        BeautifulSoup object containing the home team advanced stats.
    home_tgs : dict
        ***Dictionary containing the home team stats--VALUE UPDATED FOR CALLER BY REFERENCE***
    away_tgs : dict
        ***Dictionary containing the away team stats--VALUE UPDATED FOR CALLER BY REFERENCE***
    """
    game = games[games['br_id'] == file.split('-')[1].split('.')[0]].iloc[0]
    print(game['url'])
    
    home_tgs['game_id'] = game['id']
    away_tgs['game_id'] = game['id']
    
    home_tgs['game_br_id'] = game['br_id']
    away_tgs['game_br_id'] = game['br_id']

    away_tgs['half'] = half
    home_tgs['half'] = half
    
    next_field='minutes_played'
    away_tgs['minutes_played'] = away_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
    home_tgs['minutes_played'] = home_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
    
    next_field='team_br_id'
    home_tgs['team_br_id'] = four_factors.select('[data-stat="team_id"] > a')[0].text
    away_tgs['team_br_id'] = four_factors.select('[data-stat="team_id"] > a')[1].text
    
    next_field='field_goals'
    away_tgs['field_goals'] = away_team_basic.select('[data-stat="fg"]')[-1].text.strip()
    home_tgs['field_goals'] = home_team_basic.select('[data-stat="fg"]')[-1].text.strip()

    next_field='field_goal_attempts'
    away_tgs['field_goal_attempts'] = away_team_basic.select('[data-stat="fga"]')[-1].text.strip()
    home_tgs['field_goal_attempts'] = home_team_basic.select('[data-stat="fga"]')[-1].text.strip()
    
    next_field='field_goal_percentage'
    away_tgs['field_goal_percentage'] = away_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
    home_tgs['field_goal_percentage'] = home_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
    
    next_field='three_pointers'
    away_tgs['three_pointers'] = away_team_basic.select('[data-stat="fg3"]')[-1].text.strip()
    home_tgs['three_pointers'] = home_team_basic.select('[data-stat="fg3"]')[-1].text.strip()
    
    next_field='three_pointer_attempts'
    away_tgs['three_pointer_attempts'] = away_team_basic.select('[data-stat="fg3a"]')[-1].text.strip()
    home_tgs['three_pointer_attempts'] = home_team_basic.select('[data-stat="fg3a"]')[-1].text.strip()
    
    next_field='three_pointer_percentage'
    away_tgs['three_pointer_percentage'] = away_team_basic.select('[data-stat="fg3_pct"]')[-1].text.strip()
    home_tgs['three_pointer_percentage'] = home_team_basic.select('[data-stat="fg3_pct"]')[-1].text.strip()
    
    next_field='free_throws'
    away_tgs['free_throws'] = away_team_basic.select('[data-stat="ft"]')[-1].text.strip()
    home_tgs['free_throws'] = home_team_basic.select('[data-stat="ft"]')[-1].text.strip()
    
    next_field='free_throw_attempts'
    away_tgs['free_throw_attempts'] = away_team_basic.select('[data-stat="fta"]')[-1].text.strip()
    home_tgs['free_throw_attempts'] = home_team_basic.select('[data-stat="fta"]')[-1].text.strip()
    
    next_field='free_throw_percentage'
    away_tgs['free_throw_percentage'] = away_team_basic.select('[data-stat="ft_pct"]')[-1].text.strip()
    home_tgs['free_throw_percentage'] = home_team_basic.select('[data-stat="ft_pct"]')[-1].text.strip()
    
    next_field='rebounds'
    away_tgs['rebounds'] = away_team_basic.select('[data-stat="trb"]')[-1].text.strip()
    home_tgs['rebounds'] = home_team_basic.select('[data-stat="trb"]')[-1].text.strip()
    
    next_field='offensive_rebounds'
    away_tgs['offensive_rebounds'] = away_team_basic.select('[data-stat="orb"]')[-1].text.strip()
    home_tgs['offensive_rebounds'] = home_team_basic.select('[data-stat="orb"]')[-1].text.strip()
    
    next_field='defensive_rebounds'
    away_tgs['defensive_rebounds'] = away_team_basic.select('[data-stat="drb"]')[-1].text.strip()
    home_tgs['defensive_rebounds'] = home_team_basic.select('[data-stat="drb"]')[-1].text.strip()
    
    next_field='assists'
    away_tgs['assists'] = away_team_basic.select('[data-stat="ast"]')[-1].text.strip()
    home_tgs['assists'] = home_team_basic.select('[data-stat="ast"]')[-1].text.strip()
    
    next_field='steals'
    away_tgs['steals'] = away_team_basic.select('[data-stat="stl"]')[-1].text.strip()
    home_tgs['steals'] = home_team_basic.select('[data-stat="stl"]')[-1].text.strip()
    
    next_field='blocks'
    away_tgs['blocks'] = away_team_basic.select('[data-stat="blk"]')[-1].text.strip()
    home_tgs['blocks'] = home_team_basic.select('[data-stat="blk"]')[-1].text.strip()
    
    next_field='turnovers'
    away_tgs['turnovers'] = away_team_basic.select('[data-stat="tov"]')[-1].text.strip()
    home_tgs['turnovers'] = home_team_basic.select('[data-stat="tov"]')[-1].text.strip()
    
    next_field='personal_fouls'
    away_tgs['personal_fouls'] = away_team_basic.select('[data-stat="pf"]')[-1].text.strip()
    home_tgs['personal_fouls'] = home_team_basic.select('[data-stat="pf"]')[-1].text.strip()
    
    next_field='points'
    away_tgs['points'] = away_team_basic.select('[data-stat="pts"]')[-1].text.strip()
    home_tgs['points'] = home_team_basic.select('[data-stat="pts"]')[-1].text.strip()