import pandas as pd
import pyperclip
from io import StringIO
# TODO how to handle four factors if none (see calling func??)
def setPlayersData(game, team_br_id, team_stats_basic, team_stats_advanced) -> list:
    # Get DataFrane of basic stats
    DF_pls_basic = pd.read_html(StringIO(str(team_stats_basic)))
    DF_pls_basic = DF_pls_basic[0]
    DF_pls_basic.columns = DF_pls_basic.columns.droplevel(0)
    # remove row that function as headers
    
    # Exclude a blank header labeled as "Reserves"
    if 'Starters' in DF_pls_basic.columns:
        DF_pls_basic = DF_pls_basic[DF_pls_basic['Starters']!='Reserves']

    # Get soup object list over the same basic data
    SP_pl_basic = team_stats_basic.find('tbody').find_all('tr')
    # remove row that function as headers
    SP_pl_basic = [element for element in SP_pl_basic if 'thead' not in element.get('class', [])]
    is_starter = True
    
    if team_stats_advanced:
        # DATAFRAME VERSION
        DF_pls_advanced = pd.read_html(StringIO(str(team_stats_advanced)))
        DF_pls_advanced = DF_pls_advanced[0]
        DF_pls_advanced.columns = DF_pls_advanced.columns.droplevel(0)
        # remove row that function as headers
        DF_pls_advanced = DF_pls_advanced[DF_pls_advanced['Starters']!='Reserves']
        
        # BEAUTIFUL SOUP VERSION
        # # Get soup object list over the same basic data
        # SP_pl_advanced = team_stats_advanced.find_all('tbody')[0].find_all('tr')
        # # remove row that function as headers
        # SP_pl_advanced = [element for element in SP_pl_basic if 'thead' not in element.get('class', [])]
    
    # convert to index based loop to deal with basic and advanced simultaneously
    index=0
    pgs_list = []
    while index < len(SP_pl_basic):
        SP_player = SP_pl_basic[index]    
        if 'Reserves' in SP_player.text:
            is_starter = False
            index += 1
            continue # This is a header row, not data
        
        DF_pl_basic = DF_pls_basic.iloc[index]
        
        pgs={}

        pgs['player_br_id'] = SP_player.th.a['href'].split('/')[-1].replace('.html','')
        pgs['game_br_id'] = game['br_id']

        if str(DF_pl_basic.MP) == 'nan' \
            or str(DF_pl_basic.MP) == 'DNP' \
            or 'Did Not Play' in SP_player.text \
            or 'Did Not Dress' in SP_player.text \
            or 'Not With Team' in SP_player.text \
            or 'Player Suspended' in SP_player.text:
                
            pgs['played'] = False 
            
            if 'Did Not Play' in SP_player.text or str(DF_pl_basic.MP) == 'DNP':
                pgs['reason_for_absence'] = 'Did Not Play'
            elif 'Did Not Dress' in SP_player.text:
                pgs['reason_for_absence'] = 'Did Not Dress'
            elif 'Not With Team' in SP_player.text:
                pgs['reason_for_absence'] = 'Not With Team'
            elif 'Player Suspended' in SP_player.text:
                pgs['reason_for_absence'] = 'Player Suspended'
            elif str(DF_pl_basic.MP) == 'nan':
                pgs['reason_for_absence'] = None
            else:
                print('Error: Unhandled reason for absence')
                breakpoint() 
        else:
            pgs['played'] = True
            pgs['reason_for_absence'] = None

        pgs['started'] = is_starter
        
        if not pgs['played']:
            pgs['minutes_played'] = None
            pgs['team_br_id'] = team_br_id
            pgs['field_goal_attempts'] = None
            pgs['field_goal_percentage'] = None
            pgs['three_pointers'] = None
            pgs['three_pointer_attempts'] = None
            pgs['three_pointer_percentage'] = None
            pgs['free_throws'] = None
            pgs['free_throw_attempts'] = None
            pgs['free_throw_percentage'] = None
            pgs['rebounds'] = None
            pgs['offensive_rebounds'] = None
            pgs['defensive_rebounds'] = None
            pgs['assists'] = None
            pgs['steals'] = None
            pgs['blocks'] = None
            pgs['turnovers'] = None
            pgs['personal_fouls'] = None
            pgs['points'] = None
            pgs['plus_minus'] = None
            pgs['true_shooting_percentage'] = None
            pgs['effective_field_goal_percentage'] = None
            pgs['three_point_attempt_rate'] = None
            pgs['free_throw_attempt_rate'] = None
            pgs['offensive_rebound_percentage'] = None
            pgs['defensive_rebound_percentage'] = None
            pgs['total_rebound_percentage'] = None
            pgs['assist_percentage'] = None
            pgs['steal_percentage'] = None
            pgs['block_percentage'] = None
            pgs['turnover_percentage'] = None
            pgs['usage_percentage'] = None
            pgs['offensive_rating'] = None
            pgs['defensive_rating'] = None
            pgs['box_plus_minus'] = None

        else:
            next_field='minutes_played'; pgs['minutes_played'] = DF_pl_basic['MP']            
            next_field='team_br_id'; pgs['team_br_id'] = team_br_id
            next_field='field_goals'; pgs['field_goals'] = DF_pl_basic['FG']
            next_field='field_goal_attempts'; pgs['field_goal_attempts'] = DF_pl_basic['FGA']            
            next_field='field_goal_percentage'; pgs['field_goal_percentage'] = DF_pl_basic['FG%']            
            next_field='three_pointers'
            if '3P' in DF_pl_basic:
                pgs['three_pointers'] = DF_pl_basic['3P']            
            else:
                pgs['three_pointers'] = None
            next_field='three_pointer_attempts'
            if '3PA' in DF_pl_basic:
                pgs['three_pointer_attempts'] = DF_pl_basic['3PA']            
            else:
                pgs['three_pointer_attempts'] = None
            next_field='three_pointer_percentage'
            if '3P%' in DF_pl_basic:
                pgs['three_pointer_percentage'] = DF_pl_basic['3P%']            
            else:
                pgs['three_pointer_percentage'] = None
            next_field='free_throws'; pgs['free_throws'] = DF_pl_basic['FT']            
            next_field='free_throw_attempts'; pgs['free_throw_attempts'] = DF_pl_basic['FTA']            
            next_field='free_throw_percentage'; pgs['free_throw_percentage'] = DF_pl_basic['FT%']            
            next_field='rebounds'; pgs['rebounds'] = DF_pl_basic['TRB']            
            next_field='offensive_rebounds'; pgs['offensive_rebounds'] = DF_pl_basic['ORB']            
            next_field='defensive_rebounds'; pgs['defensive_rebounds'] = DF_pl_basic['DRB']            
            next_field='assists'; pgs['assists'] = DF_pl_basic['AST']            
            next_field='steals'; pgs['steals'] = DF_pl_basic['STL']            
            next_field='blocks'; pgs['blocks'] = DF_pl_basic['BLK']            
            next_field='turnovers'; pgs['turnovers'] = DF_pl_basic['TOV']            
            next_field='personal_fouls'; pgs['personal_fouls'] = DF_pl_basic['PF']            
            next_field='points'; pgs['points'] = DF_pl_basic['PTS']
            next_field='plus_minus'
            try:
                pgs['plus_minus'] = int(DF_pl_basic['+/-'])      
            except ValueError as e:  
                pgs['plus_minus'] = None
            except KeyError as e:  
                pgs['plus_minus'] = None
            
            #------Advanced Stats------#
            if team_stats_advanced:
                DF_pl_advanced = DF_pls_advanced.iloc[index]
                    
                next_field='true_shooting_percentage'; pgs['true_shooting_percentage'] = DF_pl_advanced['TS%']            
                next_field='effective_field_goal_percentage'; pgs['effective_field_goal_percentage'] = DF_pl_advanced['eFG%']
                next_field='three_point_attempt_rate'
                if '3PAr' in DF_pl_advanced:
                    pgs['three_point_attempt_rate'] = DF_pl_advanced['3PAr']
                else:
                    pgs['three_point_attempt_rate'] = None
                next_field='free_throw_attempt_rate'; pgs['free_throw_attempt_rate'] = DF_pl_advanced['FTr']
                next_field='offensive_rebound_percentage'; pgs['offensive_rebound_percentage'] = DF_pl_advanced['ORB%']
                next_field='defensive_rebound_percentage'; pgs['defensive_rebound_percentage'] = DF_pl_advanced['DRB%']
                next_field='total_rebound_percentage'; pgs['total_rebound_percentage'] = DF_pl_advanced['TRB%']
                next_field='assist_percentage'; pgs['assist_percentage'] = DF_pl_advanced['AST%']
                next_field='steal_percentage'; pgs['steal_percentage'] = DF_pl_advanced['STL%']
                next_field='block_percentage'; pgs['block_percentage'] = DF_pl_advanced['BLK%']
                next_field='turnover_percentage'; pgs['turnover_percentage'] = DF_pl_advanced['TOV%']
                next_field='usage_percentage'; pgs['usage_percentage'] = DF_pl_advanced['USG%']
                next_field='offensive_rating'; pgs['offensive_rating'] = DF_pl_advanced['ORtg']
                next_field='defensive_rating'; pgs['defensive_rating'] = DF_pl_advanced['DRtg']
                next_field='box_plus_minus'
                if 'BPM' in DF_pl_advanced:
                    pgs['box_plus_minus'] = DF_pl_advanced['BPM']
                else:
                    pgs['box_plus_minus'] = None
                
        index += 1
        pgs_list.append(pgs)
    
    return pgs_list

def setJSON(
    game,
    away_team_basic,
    home_team_basic,
    four_factors,
    away_team_advanced,
    home_team_advanced,
):
    """
    Set the JSON object for the PlayerGameStats object.
    """
    print(game['url'])
    
    all_players = []
    
    # away players
    all_players += setPlayersData(
        game, 
        team_br_id=game['away_team_br_id'],
        team_stats_basic=away_team_basic,
        team_stats_advanced=away_team_advanced,
    )
    
    # home players
    all_players += setPlayersData(
        game, 
        team_br_id=game['home_team_br_id'],
        team_stats_basic=home_team_basic,
        team_stats_advanced=home_team_advanced,
    )

    return all_players
    
    