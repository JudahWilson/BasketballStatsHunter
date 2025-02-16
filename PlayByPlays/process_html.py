import sys, os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
# from PlayAction import PlayAction
# from ActionMap import ActionMap
# from Play import Play
import pyperclip
import traceback
from pbp_helper import *


def process_html(game_br_id):
    """Generate Plays with their PlayActions, associating them properly to the
    game, teams, and players

    Args:
        game_br_id (str): example 202110190MIL
    """
    
    # html in file
    with open(get_pbp_filename(game_br_id), "r") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')


    ##############################################################
    # Get the teams
    ##############################################################
    away_team_br_id = name=soup.select(".thead")[1].contents[3].text
    home_team_br_id = name=soup.select(".thead")[1].contents[11].text


    ##############################################################
    # Get the plays
    ##############################################################
    plays = []
    rows = soup.find_all("tr")
    I_TIME = 0
    I_AWAY = 1
    I_JUMPBALL = 1
    I_PLUS_POINTS_AWAY = 2
    I_SCORE = 3
    I_PLUS_POINTS_HOME = 4
    I_HOME = 5
    current_quarter = None
    for row in rows:
        feet = None # distance play is from basket
        if "id" in row.attrs:
            if row["id"] in ["q1", "q2", "q3", "q4"]:
                current_quarter = int(row["id"].replace("q", ""))
        else:
            if (
                not "class" in row.attrs or row["class"] != "thead"
            ):  # If this is a data row
                tds = row.find_all("td")
                # Find the Play in the table row
                if tds != []:
                    try:
                        # JUMP BALL / GAIN_POSSESION_JUMP_BALL
                        if "Jump ball" in tds[I_JUMPBALL].text:
                            player_jump1 = get_player_br_id_from_url(tds[I_JUMPBALL].contents[1]["href"])
                            player_jump2 = get_player_br_id_from_url(tds[I_JUMPBALL].contents[3]["href"])

                            # Jump ball
                            jump_action = PlayAction(
                                PlayAction.JUMP_BALL, player_jump1
                            )
                            jump_action = PlayAction(
                                PlayAction.JUMP_BALL, player_jump2
                            )

                            player_gains_posession = get_player_br_id_from_url(tds[I_JUMPBALL].contents[5]["href"])
                            gains_posession_action = PlayAction(
                                PlayAction.GAIN_POSSESION_JUMP_BALL,
                                player_gains_posession,
                            )
                            if (
                                current_quarter == 1
                                and tds[I_TIME].text == "12:00.0"
                            ):
                                score = "0-0"
                            else:
                                score = None  # ~ don't yet have a way to get score from a jumpball play
                            plays.append(
                                Play(
                                    PlayActions=[
                                        jump_action,
                                        gains_posession_action,
                                    ],
                                    quarter=current_quarter,
                                    time=tds[I_TIME].text,
                                    score=score,
                                    distance_feet=feet,
                                )
                            )

                        elif (
                            tds[I_AWAY].text != "\xa0"
                            or tds[I_HOME].text != "\xa0"
                        ):  # If there is play-by-play content shown in the home or away columns
                            # If the content is displayed at the away side of the table
                            if tds[I_AWAY].text != "\xa0":
                                contents = tds[I_AWAY].contents
                                team_br_id = away_team_br_id
                            else:
                                contents = tds[I_HOME].contents
                                team_br_id = home_team_br_id

                            if len(contents) == 1:
                                # Quarter start--skip
                                if re.match(
                                    "Start of (1st|2nd|3rd|4th) quarter",
                                    contents[0],
                                ):
                                    continue

                                # Quarter end--skip
                                elif re.match(
                                    "End of (1st|2nd|3rd|4th) quarter", contents[0]
                                ):
                                    continue

                                # DEFENSIVE_REBOUND_BY_TEAM
                                elif (
                                    "Defensive rebound by " in contents[0]
                                    and "Team" in contents[0]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.DEFENSIVE_REBOUND_BY_TEAM,
                                        team=team_br_id,
                                    )

                                # INSTANT_REPLY_RULING_STANDS
                                elif (
                                    "Instant Replay" in contents[0]
                                    and "Ruling Stands" in contents[0]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.INSTANT_REPLY_RULING_STANDS,
                                        team=team_br_id,
                                    )

                                # INSTANT_REPLY_RULING_STANDS
                                elif "Instant Replay" in contents[0]:
                                    actions = PlayAction(
                                        action=PlayAction.INSTANT_REPLY,
                                        team=team_br_id,
                                    )

                                # KICK_BALL
                                elif "kicked ball" in contents[0]:
                                    actions = PlayAction(
                                        action=PlayAction.KICK_BALL,
                                        team=team_br_id,
                                    )

                                # FULL_TIMEOUT
                                elif "full timeout" in contents[0]:
                                    actions = PlayAction(
                                        action=PlayAction.FULL_TIMEOUT,
                                        team=team_br_id,
                                    )

                                # OFFENSIVE_REBOUND_BY_TEAM
                                elif (
                                    "Offensive rebound by Team" in contents[0]
                                    and "Team" in contents[0]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.OFFENSIVE_REBOUND_BY_TEAM,
                                        team=team_br_id,
                                    )

                                # TURNOVER_SHOT_CLOCK_VIOLATION
                                elif (
                                    "Turnover by Team (shot clock)" in contents[0]
                                    and "Team" in contents[0]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.TURNOVER_SHOT_CLOCK_VIOLATION,
                                        team=team_br_id,
                                    )

                                else:
                                    raise PlayNotYetSupportedError()

                            elif len(contents) == 2:
                                # DEFENSIVE_REBOUND
                                if (
                                    "Defensive rebound by " in contents[0]
                                    and "Team" not in contents[0]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.DEFENSIVE_REBOUND,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )

                                # DUNK_MAKE
                                elif "makes 2-pt dunk" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.DUNK_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # DUNK_MISS
                                elif "misses 2-pt dunk" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.DUNK_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # FREE_THROW_MAKE
                                elif (
                                    "makes free throw" in contents[1]
                                    or "makes flagrant free throw" in contents[1]
                                ):
                                    actions = PlayAction(
                                        action=PlayAction.FREE_THROW_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                # FREE_THROW_MISS
                                elif "misses free throw" in contents[1]:
                                    actions = PlayAction(
                                        action=PlayAction.FREE_THROW_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # LAYUP_MAKE
                                elif "makes 2-pt layup" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.LAYUP_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # LAYUP_MISS
                                elif "misses 2-pt layup" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.LAYUP_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # HOOK_SHOT_MAKE
                                elif "makes 2-pt hook shot" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.HOOK_SHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # HOOK_SHOT_MISS
                                elif "misses 2-pt hook shot" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    actions = PlayAction(
                                        action=PlayAction.HOOK_SHOT_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # OFFENSIVE_REBOUND
                                elif "Offensive rebound by " in contents[0]:
                                    actions = PlayAction(
                                        action=PlayAction.OFFENSIVE_REBOUND,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )

                                # THREE_POINT_JUMPSHOT_MAKE
                                elif "makes 3-pt jump shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    actions = PlayAction(
                                        action=PlayAction.THREE_POINT_JUMPSHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # THREE_POINT_JUMPSHOT_MISS
                                elif "misses 3-pt jump shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    actions = PlayAction(
                                        action=PlayAction.THREE_POINT_JUMPSHOT_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # TWO_POINT_JUMPSHOT_MAKE
                                elif "makes 2-pt jump shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    actions = PlayAction(
                                        action=PlayAction.TWO_POINT_JUMPSHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )

                                # TWO_POINT_JUMPSHOT_MISS
                                elif "misses 2-pt jump shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    actions = PlayAction(
                                        action=PlayAction.TWO_POINT_JUMPSHOT_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                else:
                                    raise PlayNotYetSupportedError()

                            elif len(contents) == 3:
                                # LEAVE_THE_GAME / ENTER_THE_GAME
                                if "enters the game for" in contents[1]:
                                    leave_action = PlayAction(
                                        action=PlayAction.LEAVE_THE_GAME,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    enter_action = PlayAction(
                                        action=PlayAction.ENTER_THE_GAME,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [leave_action, enter_action]

                                # TURNOVER_BAD_PASS
                                elif "Turnover by" in contents[0]:
                                    actions = PlayAction(
                                        action=PlayAction.TURNOVER_BAD_PASS,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                else:
                                    raise PlayNotYetSupportedError()

                            elif len(contents) == 4:
                                # DUNK_MAKE / ASSIST
                                if (
                                    "makes 2-pt dunk" in contents[1]
                                    and "assist by" in contents[1]
                                ):
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    dunk_action = PlayAction(
                                        action=PlayAction.DUNK_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    assist_action = PlayAction(
                                        action=ActionMap.assist,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [dunk_action, assist_action]

                                # LAYUP_MISS / BLOCK
                                elif "misses 2-pt layup" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    miss_action = PlayAction(
                                        action=PlayAction.LAYUP_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    block_action = PlayAction(
                                        action=PlayAction.BLOCK,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [miss_action, block_action]

                                # LAYUP_MISS / BLOCK
                                elif "misses 2-pt dunk" in contents[1]:
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    miss_action = PlayAction(
                                        action=PlayAction.DUNK_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    block_action = PlayAction(
                                        action=PlayAction.BLOCK,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [miss_action, block_action]

                                # LAYUP_MAKE / ASSIST
                                elif (
                                    "makes 2-pt layup" in contents[1]
                                    and "assist by" in contents[1]
                                ):
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    layup_action = PlayAction(
                                        action=PlayAction.LAYUP_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    assist_action = PlayAction(
                                        action=PlayAction.ASSIST,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [layup_action, assist_action]

                                # HOOK_SHOT_MAKE / ASSIST
                                elif (
                                    "makes 2-pt hook shot" in contents[1]
                                    and "assist by" in contents[1]
                                ):
                                    if "at rim" in contents[1]:
                                        feet = 0
                                    else:
                                        feet = int(
                                            re.match(
                                                r".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                    layup_action = PlayAction(
                                        action=PlayAction.HOOK_SHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    assist_action = PlayAction(
                                        action=PlayAction.ASSIST,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [layup_action, assist_action]

                                # THREE_POINT_JUMPSHOT_MAKE / ASSIST
                                elif (
                                    "makes 3-pt jump shot" in contents[1]
                                    and "assist by" in contents[1]
                                ):
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    three_point_make_action = PlayAction(
                                        action=PlayAction.THREE_POINT_JUMPSHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    assist_action = PlayAction(
                                        action=PlayAction.ASSIST,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [
                                        three_point_make_action,
                                        assist_action,
                                    ]

                                # TWO_POINT_JUMPSHOT_MAKE / ASSIST
                                elif (
                                    "makes 2-pt jump shot" in contents[1]
                                    and "assist by" in contents[1]
                                ):
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    three_point_make_action = PlayAction(
                                        action=PlayAction.TWO_POINT_JUMPSHOT_MAKE,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    assist_action = PlayAction(
                                        action=PlayAction.ASSIST,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [
                                        three_point_make_action,
                                        assist_action,
                                    ]

                                # TWO_POINT_JUMPSHOT_MISS / BLOCK
                                elif "misses 2-pt jump shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    miss_action = PlayAction(
                                        action=PlayAction.TWO_POINT_JUMPSHOT_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    block_action = PlayAction(
                                        action=PlayAction.BLOCK,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [miss_action, block_action]

                                # HOOK_SHOT_MISS / BLOCK
                                elif "misses 2-pt hook shot" in contents[1]:
                                    feet = int(
                                        re.match(
                                            r".* from (\d+) ft.*", contents[1]
                                        ).groups(1)[0]
                                    )
                                    miss_action = PlayAction(
                                        action=PlayAction.HOOK_SHOT_MISS,
                                        player_br_id=get_player_br_id_from_url(contents[0]["href"])
                                    )
                                    block_action = PlayAction(
                                        action=PlayAction.BLOCK,
                                        player_br_id=get_player_br_id_from_url(contents[2]["href"])
                                    )
                                    actions = [miss_action, block_action]
                                else:
                                    raise PlayNotYetSupportedError()
                            elif len(contents) == 5:
                                # BLOCKING_FOUL_COMMIT / BLOCKING_FOUL_DRAW
                                if "Shooting foul by" in contents[0]:
                                    commit_foul_action = PlayAction(
                                        action=PlayAction.BLOCKING_FOUL_COMMIT,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                    draw_foul_action = PlayAction(
                                        action=PlayAction.BLOCKING_FOUL_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )
                                    actions = [commit_foul_action, draw_foul_action]

                                # LOOSE_BALL_FOUL_COMMIT / LOOSE_BALL_FOUL_DRAW
                                elif "Loose ball foul by" in contents[0]:
                                    commit_foul_action = PlayAction(
                                        action=PlayAction.LOOSE_BALL_FOUL_COMMIT,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                    draw_foul_action = PlayAction(
                                        action=PlayAction.LOOSE_BALL_FOUL_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )
                                    actions = [commit_foul_action, draw_foul_action]

                                # OFFENSIVE_FOUL_COMMIT / STEAL
                                elif (
                                    "Offensive foul by" in contents[0]
                                    and "drawn by" in contents[2]
                                ):
                                    offensive_commit_action = PlayAction(
                                        action=PlayAction.OFFENSIVE_FOUL_COMMIT,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )

                                    offensive_draw_action = PlayAction(
                                        action=PlayAction.OFFENSIVE_FOUL_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )

                                    actions = [
                                        offensive_commit_action,
                                        offensive_draw_action,
                                    ]

                                # PERSONAL_FOUL_COMMIT / PERSONAL_FOUL_DRAW
                                elif (
                                    "Personal take foul by" in contents[0]
                                    or "Personal foul by" in contents[0]
                                ):
                                    commit_foul_action = PlayAction(
                                        action=PlayAction.PERSONAL_FOUL_COMMIT,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                    draw_foul_action = PlayAction(
                                        action=PlayAction.PERSONAL_FOUL_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )
                                    actions = [commit_foul_action, draw_foul_action]

                                # SHOOTING_FOUL_COMMIT / SHOOTING_FOUL_DRAW
                                elif "Shooting foul by" in contents[0]:
                                    commit_foul_action = PlayAction(
                                        action=PlayAction.SHOOTING_FOUL_COMMIT,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                    draw_foul_action = PlayAction(
                                        action=PlayAction.SHOOTING_FOUL_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )
                                    actions = [commit_foul_action, draw_foul_action]

                                # TURNOVER_BAD_PASS / STEAL
                                elif (
                                    "Turnover by" in contents[0]
                                    and "bad pass; steal by" in contents[2]
                                ):
                                    player_turnover = get_player_br_id_from_url(contents[1]["href"])
                                    turnover_action = PlayAction(
                                        action=PlayAction.TURNOVER_BAD_PASS,
                                        player=player_turnover,
                                    )

                                    player_steal = get_player_br_id_from_url(contents[3]["href"])
                                    steal_action = PlayAction(
                                        action=PlayAction.STEAL,
                                        player=player_steal,
                                    )

                                    actions = [turnover_action, steal_action]

                                # TURNOVER_LOST_BALL / STEAL
                                elif (
                                    "Turnover by" in contents[0]
                                    and "lost ball; steal by" in contents[2]
                                ):
                                    turnover_action = PlayAction(
                                        action=PlayAction.TURNOVER_LOST_BALL,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )

                                    steal_action = PlayAction(
                                        action=PlayAction.STEAL,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )

                                    actions = [turnover_action, steal_action]
                                # FLAGRANT_FOUL_TYPE_1 / FLAGRANT_FOUL_TYPE_1_DRAW
                                elif "Flagrant foul type 1 by" in contents[0]:
                                    commit_foul_action = PlayAction(
                                        action=PlayAction.FLAGRANT_FOUL_TYPE_1,
                                        player_br_id=get_player_br_id_from_url(contents[1]["href"])
                                    )
                                    draw_foul_action = PlayAction(
                                        action=PlayAction.FLAGRANT_FOUL_TYPE_1_DRAW,
                                        player_br_id=get_player_br_id_from_url(contents[3]["href"])
                                    )
                                    actions = [commit_foul_action, draw_foul_action]
                                else:
                                    raise PlayNotYetSupportedError()
                            else:
                                raise PlayNotYetSupportedError()

                            plays.append(
                                Play(
                                    PlayActions=actions,
                                    quarter=current_quarter,
                                    time=tds[I_TIME].text,
                                    score=tds[I_SCORE].text,
                                    distance_feet=feet,
                                )
                            )
                        else:
                            raise PlayNotYetSupportedError()
                    except PlayNotYetSupportedError as e:
                        import traceback

                        quarter = current_quarter
                        time = tds[I_TIME]
                        html = str(row)
                        error = str(e)
                        tb = traceback.format_exc()
                        is_play_not_supported = True

                        print(f"url -- {url}")
                        print(f"quarter -- {quarter}")
                        print(f"time -- {time}")
                        print(f"html -- {html}")
                        print(f"error -- {error}")
                        print(f"traceback -- {tb}")
                        print(f"is_play_not_supported -- {is_play_not_supported}")
                        
                    except Exception as e:
                        import traceback

                        quarter = current_quarter
                        time = tds[I_TIME]
                        html = str(row)
                        error = str(e)
                        tb = traceback.format_exc()
                        is_play_not_supported = False

                        print(f"url -- {url}")
                        print(f"quarter -- {quarter}")
                        print(f"time -- {time}")
                        print(f"html -- {html}")
                        print(f"error -- {error}")
                        print(f"traceback -- {tb}")
                        print(f"is_play_not_supported -- {is_play_not_supported}")

