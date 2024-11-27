import pandas as pd
import pyperclip
from io import StringIO

def setJSON(games, away_team_basic, home_team_basic, four_factors, inactive_players, away_team_advanced, home_team_advanced, home_tgs, away_tgs, file, year):
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
    
    next_field='team_br_id'
    away_tgs['team_br_id'] = away_team_basic.attrs['id'].split('-')[1]
    home_tgs['team_br_id'] = home_team_basic.attrs['id'].split('-')[1]
    
    next_field='minutes_played'
    away_tgs['minutes_played'] = away_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
    home_tgs['minutes_played'] = home_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
    
    next_field='field_goals'
    away_tgs['field_goals'] = away_team_basic.select('[data-stat="fg"]')[-1].text.strip()
    home_tgs['field_goals'] = home_team_basic.select('[data-stat="fg"]')[-1].text.strip()

    next_field='field_goal_attempts'
    away_tgs['field_goal_attempts'] = away_team_basic.select('[data-stat="fga"]')[-1].text.strip()
    home_tgs['field_goal_attempts'] = home_team_basic.select('[data-stat="fga"]')[-1].text.strip()
    
    next_field='field_goal_percentage'
    away_tgs['field_goal_percentage'] = away_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
    home_tgs['field_goal_percentage'] = home_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
    
    if 'three_pointers' in away_tgs:
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
    
    if four_factors:        
        next_field='pace_factor'
        away_tgs['pace_factor'] = four_factors.select('[data-stat="pace"]')[1].text.strip()
        home_tgs['pace_factor'] = four_factors.select('[data-stat="pace"]')[2].text.strip()
        
        next_field='ft_per_fga'
        away_tgs['ft_per_fga'] = four_factors.select('[data-stat="ft_rate"]')[1].text.strip()
        home_tgs['ft_per_fga'] = four_factors.select('[data-stat="ft_rate"]')[2].text.strip()

    
    #------Advanced Stats------#
    if away_team_advanced:
        next_field='true_shooting_percentage'
        away_tgs['true_shooting_percentage'] = away_team_advanced.select('[data-stat="ts_pct"]')[-1].text.strip()
        home_tgs['true_shooting_percentage'] = home_team_advanced.select('[data-stat="ts_pct"]')[-1].text.strip()
        
        next_field='effective_field_goal_percentage'
        away_tgs['effective_field_goal_percentage'] = away_team_advanced.select('[data-stat="efg_pct"]')[-1].text.strip()
        home_tgs['effective_field_goal_percentage'] = home_team_advanced.select('[data-stat="efg_pct"]')[-1].text.strip()
        
        next_field='three_point_attempt_rate'
        away_tgs['three_point_attempt_rate'] = away_team_advanced.select('[data-stat="fg3a_per_fga_pct"]')[-1].text.strip()
        home_tgs['three_point_attempt_rate'] = home_team_advanced.select('[data-stat="fg3a_per_fga_pct"]')[-1].text.strip()
        
        next_field='free_throw_attempt_rate'
        away_tgs['free_throw_attempt_rate'] = away_team_advanced.select('[data-stat="fta_per_fga_pct"]')[-1].text.strip()
        home_tgs['free_throw_attempt_rate'] = home_team_advanced.select('[data-stat="fta_per_fga_pct"]')[-1].text.strip()
        
        next_field='offensive_rebound_percentage'
        away_tgs['offensive_rebound_percentage'] = away_team_advanced.select('[data-stat="orb_pct"]')[-1].text.strip()
        home_tgs['offensive_rebound_percentage'] = home_team_advanced.select('[data-stat="orb_pct"]')[-1].text.strip()
        
        next_field='defensive_rebound_percentage'
        away_tgs['defensive_rebound_percentage'] = away_team_advanced.select('[data-stat="drb_pct"]')[-1].text.strip()
        home_tgs['defensive_rebound_percentage'] = home_team_advanced.select('[data-stat="drb_pct"]')[-1].text.strip()
        
        next_field='total_rebound_percentage'
        away_tgs['total_rebound_percentage'] = away_team_advanced.select('[data-stat="trb_pct"]')[-1].text.strip()
        home_tgs['total_rebound_percentage'] = home_team_advanced.select('[data-stat="trb_pct"]')[-1].text.strip()
        
        next_field='assist_percentage'
        away_tgs['assist_percentage'] = away_team_advanced.select('[data-stat="ast_pct"]')[-1].text.strip()
        home_tgs['assist_percentage'] = home_team_advanced.select('[data-stat="ast_pct"]')[-1].text.strip()
        
        next_field='steal_percentage'
        away_tgs['steal_percentage'] = away_team_advanced.select('[data-stat="stl_pct"]')[-1].text.strip()
        home_tgs['steal_percentage'] = home_team_advanced.select('[data-stat="stl_pct"]')[-1].text.strip()
        
        next_field='block_percentage'
        away_tgs['block_percentage'] = away_team_advanced.select('[data-stat="blk_pct"]')[-1].text.strip()
        home_tgs['block_percentage'] = home_team_advanced.select('[data-stat="blk_pct"]')[-1].text.strip()
        
        next_field='turnover_percentage'
        away_tgs['turnover_percentage'] = away_team_advanced.select('[data-stat="tov_pct"]')[-1].text.strip()
        home_tgs['turnover_percentage'] = home_team_advanced.select('[data-stat="tov_pct"]')[-1].text.strip()
        
        next_field='usage_percentage'
        away_tgs['usage_percentage'] = away_team_advanced.select('[data-stat="usg_pct"]')[-1].text.strip()
        home_tgs['usage_percentage'] = home_team_advanced.select('[data-stat="usg_pct"]')[-1].text.strip()
        
        next_field='offensive_rating'
        away_tgs['offensive_rating'] = away_team_advanced.select('[data-stat="off_rtg"]')[-1].text.strip()
        home_tgs['offensive_rating'] = home_team_advanced.select('[data-stat="off_rtg"]')[-1].text.strip()
        
        next_field='defensive_rating'
        away_tgs['defensive_rating'] = away_team_advanced.select('[data-stat="def_rtg"]')[-1].text.strip()
        home_tgs['defensive_rating'] = home_team_advanced.select('[data-stat="def_rtg"]')[-1].text.strip()
        
    next_field='inactive_players'
    away_tgs['inactive_players'] = []
    home_tgs['inactive_players'] = []
    away_or_home = None
    if inactive_players:
        for tag in inactive_players.select('span, a'):
            if tag.name == 'span':
                if away_or_home is None:
                    away_or_home = 'away'
                elif away_or_home == 'away':
                    away_or_home = 'home'
            
            elif tag.name == 'a':
                if away_or_home == 'away':
                    away_tgs['inactive_players'].append(tag['href'].split('/')[-1].replace('.html',''))
                elif away_or_home == 'home':
                    home_tgs['inactive_players'].append(tag['href'].split('/')[-1].replace('.html',''))
    else:
        away_tgs['inactive_players'] = []
        home_tgs['inactive_players'] = []