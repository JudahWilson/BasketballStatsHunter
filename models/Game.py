import sys, os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from Action import Action
from Play import Play
from Instance_Player_Game import Instance_Player_Game
from Instance_Team_Game import Instance_Team_Game
import pyperclip

class Game():

    def __init__(self, url):
        self.url = url
        self.datetime = None
        if url.startswith('https'):   
            # html in website
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
        else:
            # html in file
            with open(url,'r') as f:
                soup = f.read()
        
        self.soup = soup # for debugging purposes

        table_play_by_play = soup.find('table')

        ##############################################################
        # Get the teams
        ##############################################################
        self.away_team = Instance_Team_Game(name=table_play_by_play.select('.thead')[1].contents[3].text)
        self.home_team = Instance_Team_Game(name=table_play_by_play.select('.thead')[1].contents[11].text)

        ##############################################################
        # Get the players
        ##############################################################
        boxscore_url = self.url.replace(r'pbp/', '')
        boxscore_soup = BeautifulSoup(requests.get(boxscore_url).text, 'html.parser')
        away_table1 = boxscore_soup.find_all('table')[0]
        self.away_players = []
        for player_th in away_table1.find_all('th',{'class':'left'}):
            if 'data-append-csv' in player_th.attrs:
                self.away_players.append(player_th['data-append-csv'])

        home_table1 = boxscore_soup.find_all('table')[8]
        self.home_players = []
        for player_th in home_table1.find_all('th', {'class': 'left'}):
            if 'data-append-csv' in player_th.attrs:
                self.home_players.append(player_th['data-append-csv'])

        ##############################################################
        # Get the plays
        ##############################################################
        self.plays = []
        rows = table_play_by_play.find_all('tr')
        time_index = 0
        away_index = 1
        jumpball_index = 1
        plus_points_away_index = 2
        score_index = 3
        plus_points_home_index = 4
        home_index = 5
        for row in rows:
            if 'id' in row.attrs:
                if row['id'] in ['q1', 'q2', 'q3', 'q4']:
                    current_quarter = int(row['id'].replace('q', ''))
            else:
                if not 'class' in row.attrs or row['class'] != 'thead':  # If this is a data row
                    tds = row.find_all('td')
                    # Find the Play in the table row
                    if tds != []:

                        # JUMP BALL / GAIN_POSSESION_JUMP_BALL
                        if 'Jump ball' in tds[jumpball_index].text:
                            player_jump1 = Instance_Player_Game(url=tds[jumpball_index].contents[1]['href'])
                            player_jump2 = Instance_Player_Game(url=tds[jumpball_index].contents[3]['href'])
                            jump_action = Action(Action.JUMP_BALL, [player_jump1, player_jump2])

                            player_gains_posession = Instance_Player_Game(url=tds[jumpball_index].contents[5]['href'])
                            gains_posession_action = Action(Action.GAIN_POSSESION_JUMP_BALL, player_gains_posession)
                            if current_quarter == 1 and tds[time_index].text == '12:00.0':
                                score = '0-0'
                            else:
                                score = None  # ~ don't yet have a way to get score from a jumpball play
                            self.plays.append(Play(actions=[jump_action, gains_posession_action],
                                                    quarter=current_quarter, time=tds[time_index].text,
                                                    score=score))

                        elif tds[away_index].text != '\xa0' or tds[home_index].text != '\xa0':  # If there is play-by-play content shown in the home or away columns

                            # If the content is displayed at the away side of the table
                            if tds[away_index].text != '\xa0':
                                contents = tds[away_index].contents
                                current_team = self.away_team
                            else:
                                contents = tds[home_index].contents
                                current_team = self.home_team

                            if len(contents) == 1:
                                # Quarter start--skip
                                if re.match('Start of (1st|2nd|3rd|4th) quarter', contents[0]):
                                    continue

                                # Quarter end--skip
                                elif re.match('End of (1st|2nd|3rd|4th) quarter', contents[0]):
                                    continue

                                # DEFENSIVE_REBOUND_BY_TEAM
                                elif 'Defensive rebound by ' in contents[0] and 'Team' in contents[0]:
                                    actions = Action(action=Action.DEFENSIVE_REBOUND_BY_TEAM, team=current_team)

                                # INSTANT_REPLY_RULING_STANDS
                                elif 'Instant Replay' in contents[0] and 'Ruling Stands' in contents[0]:
                                    actions = Action(action=Action.INSTANT_REPLY_RULING_STANDS, team=current_team)

                                # INSTANT_REPLY_RULING_STANDS
                                elif 'Instant Replay' in contents[0]:
                                    actions = Action(action=Action.INSTANT_REPLY, team=current_team)

                                # KICK_BALL
                                elif 'kicked ball' in contents[0]:
                                    actions = Action(action=Action.KICK_BALL, team=current_team)

                                # FULL_TIMEOUT
                                elif 'full timeout' in contents[0]:
                                    actions = Action(action=Action.FULL_TIMEOUT, team=current_team)

                                # OFFENSIVE_REBOUND_BY_TEAM
                                elif 'Offensive rebound by Team' in contents[0] and 'Team' in contents[0]:
                                    actions = Action(action=Action.OFFENSIVE_REBOUND_BY_TEAM, team=current_team)

                                # TURNOVER_SHOT_CLOCK_VIOLATION
                                elif 'Turnover by Team (shot clock)' in contents[0] and 'Team' in contents[0]:
                                    actions = Action(action=Action.TURNOVER_SHOT_CLOCK_VIOLATION, team=current_team)

                                else:
                                    print('Data row not yet processable: ' + str(row))
                                    breakpoint()

                            elif len(contents) == 2:

                                # DEFENSIVE_REBOUND
                                if 'Defensive rebound by ' in contents[0] and 'Team' not in contents[0]:
                                    actions = Action(action=Action.DEFENSIVE_REBOUND,
                                                     players=Instance_Player_Game(url=contents[1]['href']))

                                # DUNK_MAKE
                                elif 'makes 2-pt dunk' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.DUNK_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # DUNK_MISS
                                elif 'misses 2-pt dunk' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.DUNK_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # FREE_THROW_MAKE
                                elif 'makes free throw' in contents[1] or 'makes flagrant free throw' in contents[1]:
                                    actions = Action(action=Action.FREE_THROW_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']))
                                # FREE_THROW_MISS
                                elif 'misses free throw' in contents[1]:
                                    actions = Action(action=Action.FREE_THROW_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']))

                                # LAYUP_MAKE
                                elif 'makes 2-pt layup' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.LAYUP_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # LAYUP_MISS
                                elif 'misses 2-pt layup' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.LAYUP_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # HOOK_SHOT_MAKE
                                elif 'makes 2-pt hook shot' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.HOOK_SHOT_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # HOOK_SHOT_MISS
                                elif 'misses 2-pt hook shot' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.HOOK_SHOT_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # OFFENSIVE_REBOUND
                                elif 'Offensive rebound by ' in contents[0]:
                                    actions = Action(action=Action.OFFENSIVE_REBOUND,
                                                     players=Instance_Player_Game(url=contents[1]['href']))

                                # THREE_POINT_JUMPSHOT_MAKE
                                elif 'makes 3-pt jump shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.THREE_POINT_JUMPSHOT_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # THREE_POINT_JUMPSHOT_MISS
                                elif 'misses 3-pt jump shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.THREE_POINT_JUMPSHOT_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # TWO_POINT_JUMPSHOT_MAKE
                                elif 'makes 2-pt jump shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.TWO_POINT_JUMPSHOT_MAKE,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)

                                # TWO_POINT_JUMPSHOT_MISS
                                elif 'misses 2-pt jump shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    actions = Action(action=Action.TWO_POINT_JUMPSHOT_MISS,
                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                else:
                                    print('Data row not yet processable: ' + str(row))
                                    breakpoint()

                            elif len(contents) == 3:

                                # LEAVE_THE_GAME / ENTER_THE_GAME
                                if 'enters the game for' in contents[1]:
                                    leave_action = Action(action=Action.LEAVE_THE_GAME,
                                                          players=Instance_Player_Game(url=contents[0]['href']))
                                    enter_action = Action(action=Action.ENTER_THE_GAME,
                                                          players=Instance_Player_Game(url=contents[2]['href']))
                                    actions=[leave_action,enter_action]

                                # TURNOVER_BAD_PASS
                                elif 'Turnover by' in contents[0]:
                                    actions = Action(action=Action.TURNOVER_BAD_PASS,
                                                     players=Instance_Player_Game(url=contents[1]['href']))
                                else:
                                    print('Data row not yet processable: ' + str(row))
                                    breakpoint()

                            elif len(contents) == 4:
                                # DUNK_MAKE / ASSIST
                                if 'makes 2-pt dunk' in contents[1] and 'assist by' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    dunk_action = Action(action=Action.DUNK_MAKE,
                                                         players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    assist_action = Action(action=Action.ASSIST,
                                                           players=Instance_Player_Game(url=contents[2]['href']))
                                    actions=[dunk_action,assist_action]

                                # LAYUP_MISS / BLOCK
                                elif 'misses 2-pt layup' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    miss_action = Action(action=Action.LAYUP_MISS,
                                                         players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    block_action = Action(action=Action.BLOCK,
                                                          players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [miss_action, block_action]

                                # LAYUP_MISS / BLOCK
                                elif 'misses 2-pt dunk' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    miss_action = Action(action=Action.DUNK_MISS,
                                                         players=Instance_Player_Game(url=contents[0]['href']),
                                                         feet=feet)
                                    block_action = Action(action=Action.BLOCK,
                                                          players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [miss_action, block_action]

                                # LAYUP_MAKE / ASSIST
                                elif 'makes 2-pt layup' in contents[1] and 'assist by' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    layup_action = Action(action=Action.LAYUP_MAKE,
                                                          players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    assist_action = Action(action=Action.ASSIST,
                                                           players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [layup_action, assist_action]

                                # HOOK_SHOT_MAKE / ASSIST
                                elif 'makes 2-pt hook shot' in contents[1] and 'assist by' in contents[1]:
                                    if 'at rim' in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    layup_action = Action(action=Action.HOOK_SHOT_MAKE,
                                                          players=Instance_Player_Game(url=contents[0]['href']),
                                                          feet=feet)
                                    assist_action = Action(action=Action.ASSIST,
                                                           players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [layup_action, assist_action]

                                # THREE_POINT_JUMPSHOT_MAKE / ASSIST
                                elif 'makes 3-pt jump shot' in contents[1] and 'assist by' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    three_point_make_action = Action(action=Action.THREE_POINT_JUMPSHOT_MAKE,
                                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    assist_action = Action(action=Action.ASSIST,
                                                           players=Instance_Player_Game(url=contents[2]['href']))
                                    actions=[three_point_make_action,assist_action]

                                # TWO_POINT_JUMPSHOT_MAKE / ASSIST
                                elif 'makes 2-pt jump shot' in contents[1] and 'assist by' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    three_point_make_action = Action(action=Action.TWO_POINT_JUMPSHOT_MAKE,
                                                                     players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    assist_action = Action(action=Action.ASSIST,
                                                           players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [three_point_make_action, assist_action]

                                # TWO_POINT_JUMPSHOT_MISS / BLOCK
                                elif 'misses 2-pt jump shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    miss_action = Action(action=Action.TWO_POINT_JUMPSHOT_MISS,
                                                         players=Instance_Player_Game(url=contents[0]['href']), feet=feet)
                                    block_action = Action(action=Action.BLOCK,
                                                          players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [miss_action, block_action]

                                # HOOK_SHOT_MISS / BLOCK
                                elif 'misses 2-pt hook shot' in contents[1]:
                                    feet = int(re.match('.* from (\d+) ft.*', contents[1]).groups(1)[0])
                                    miss_action = Action(action=Action.HOOK_SHOT_MISS,
                                                         players=Instance_Player_Game(url=contents[0]['href']),
                                                         feet=feet)
                                    block_action = Action(action=Action.BLOCK,
                                                          players=Instance_Player_Game(url=contents[2]['href']))
                                    actions = [miss_action, block_action]
                                else:
                                    print('Data row not yet processable: ' + str(row))
                                    breakpoint()
                            elif len(contents) == 5:
                                # BLOCKING_FOUL_COMMIT / BLOCKING_FOUL_DRAW
                                if 'Shooting foul by' in contents[0]:
                                    commit_foul_action = Action(action=Action.BLOCKING_FOUL_COMMIT,
                                                                players=Instance_Player_Game(url=contents[1]['href']))
                                    draw_foul_action = Action(action=Action.BLOCKING_FOUL_DRAW,
                                                              players=Instance_Player_Game(url=contents[3]['href']))
                                    actions = [commit_foul_action, draw_foul_action]

                                # LOOSE_BALL_FOUL_COMMIT / LOOSE_BALL_FOUL_DRAW
                                elif 'Loose ball foul by' in contents[0]:
                                    commit_foul_action = Action(action=Action.LOOSE_BALL_FOUL_COMMIT,
                                                                players=Instance_Player_Game(url=contents[1]['href']))
                                    draw_foul_action = Action(action=Action.LOOSE_BALL_FOUL_DRAW,
                                                              players=Instance_Player_Game(url=contents[3]['href']))
                                    actions = [commit_foul_action, draw_foul_action]

                                # OFFENSIVE_FOUL_COMMIT / STEAL
                                elif 'Offensive foul by' in contents[0] and 'drawn by' in contents[2]:
                                    offensive_commit_action = Action(action=Action.OFFENSIVE_FOUL_COMMIT,
                                                                     players=Instance_Player_Game(url=contents[1]['href']))

                                    offensive_draw_action = Action(action=Action.OFFENSIVE_FOUL_DRAW,
                                                                   players=Instance_Player_Game(url=contents[3]['href']))

                                    actions = [offensive_commit_action, offensive_draw_action]

                                # PERSONAL_FOUL_COMMIT / PERSONAL_FOUL_DRAW
                                elif 'Personal take foul by' in contents[0] or 'Personal foul by' in contents[0]:
                                    commit_foul_action = Action(action=Action.PERSONAL_FOUL_COMMIT,
                                                                players=Instance_Player_Game(url=contents[1]['href']))
                                    draw_foul_action = Action(action=Action.PERSONAL_FOUL_DRAW,
                                                              players=Instance_Player_Game(url=contents[3]['href']))
                                    actions = [commit_foul_action, draw_foul_action]

                                # SHOOTING_FOUL_COMMIT / SHOOTING_FOUL_DRAW
                                elif 'Shooting foul by' in contents[0]:
                                    commit_foul_action = Action(action=Action.SHOOTING_FOUL_COMMIT,
                                                                players=Instance_Player_Game(url=contents[1]['href']))
                                    draw_foul_action = Action(action=Action.SHOOTING_FOUL_DRAW,
                                                              players=Instance_Player_Game(url=contents[3]['href']))
                                    actions = [commit_foul_action, draw_foul_action]

                                # TURNOVER_BAD_PASS / STEAL
                                elif 'Turnover by' in contents[0] and 'bad pass; steal by' in contents[2]:
                                    player_turnover = Instance_Player_Game(url=contents[1]['href'])
                                    turnover_action = Action(action=Action.TURNOVER_BAD_PASS, players=player_turnover)

                                    player_steal = Instance_Player_Game(url=contents[3]['href'])
                                    steal_action = Action(action=Action.STEAL, players=player_steal)

                                    actions=[turnover_action,steal_action]

                                # TURNOVER_LOST_BALL / STEAL
                                elif 'Turnover by' in contents[0] and 'lost ball; steal by' in contents[2]:
                                    turnover_action = Action(action=Action.TURNOVER_LOST_BALL,
                                                             players=Instance_Player_Game(url=contents[1]['href']))

                                    steal_action = Action(action=Action.STEAL, players=Instance_Player_Game(url=contents[3]['href']))

                                    actions = [turnover_action, steal_action]
                                # FLAGRANT_FOUL_TYPE_1 / FLAGRANT_FOUL_TYPE_1_DRAW
                                elif 'Flagrant foul type 1 by' in contents[0]:
                                    commit_foul_action = Action(action=Action.FLAGRANT_FOUL_TYPE_1,
                                                                players=Instance_Player_Game(
                                                                    url=contents[1]['href']))
                                    draw_foul_action = Action(action=Action.FLAGRANT_FOUL_TYPE_1_DRAW,
                                                              players=Instance_Player_Game(url=contents[3]['href']))
                                    actions = [commit_foul_action, draw_foul_action]
                                else:
                                    print('Data row not yet processable: ' + str(row))
                                    breakpoint()
                            else:
                                print('Data row not yet processable: ' + str(row))
                                breakpoint()

                            self.plays.append(Play(actions=actions, quarter=current_quarter,
                                                    time=tds[time_index].text, score=tds[score_index].text))
                        else:
                            print('Data row not yet processable: ' + str(row))
                            breakpoint()
            '''except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('Error when processing row: ' + str(row))
                print(exc_type, fname, exc_tb.tb_lineno)'''

    def __str__(self):
        play_str_list = []
        for play in self.plays:
            play_str_list.append('Q' + str(play.quarter) + ' ' + play.time + '\n' + str(play))

        return '\n\n'.join(play_str_list)
    
    def __iter__(self):
        # Build the data to save
        for play in self.plays:
            row_builder = {}
            row_builder['Quarter'] = 'Q' + str(play.quarter)
            row_builder['Time'] = play.time
            row_builder['Actions'] = ' | '.join(list(play))
            yield row_builder
            
    def __DataFrame__(self):
        return pd.DataFrame(list(self))
    
    def copy(self):
        pyperclip.copy(str(self))
        
    def excel(self):
        # Build the data to save
        excel_builder = []
        for play in self.plays:
            row_builder = {}
            row_builder['Quarter'] = 'Q' + str(play.quarter)
            row_builder['Time'] = play.time
            row_builder['Actions'] = ' | '.join(list(play))
            excel_builder.append(row_builder)
        
        # Save the data
        pd.DataFrame(excel_builder).to_excel('game.xlsx', index=False)
        
        # Open the file with excel
        os.startfile('game.xlsx')

    def _get_team_of_player(self,player_id):
        assert player_id in self.away_team or player_id in self.home_team

        if '' in self.away_players:
            return self.away_team
        else:
            return self.home_team
