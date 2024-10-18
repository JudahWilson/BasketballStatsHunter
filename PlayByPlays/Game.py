"""WORKFLOW
- Get play by play data
    - loop through all plays scan the play's html content to determine the
      actions, time, distance, and players per action involved 
    - if the code is able to recognize the play, it will generate new
      PlayAction(s) objects and associate them to a new Play object with all
      relavent data applicable to these respective objects. There is a list of
      plays that are appended with each play as they are scanned
    - if the play's content is not recogized, breakpoint for manual inspection
      DB. Afterwards a new if condition will be added to handle the newly
      and make a convenient segway to save new ActionMap entries needed in the
      reognized play
    - after all plays are scanned and if there were no issues recognizing and
      saving each play, the list of plays with their respective PlayAction(s)
      will be flushed to the DB
      
NOTE: each python object corresponds to a DB table. they can fully resembling
all literal columns data. however, additionally, each related table is
accessible directly as an attribute of the object for additional convenience
"""

"""TODO
- define all models including ActionMap WITH db columns PLUS assign reference of related python objects for coding convenience 
    - ActionMap
    - Play
    - PlayAction
    - TeamGameStats
    - TeamGameQuarterStats
    - TeamGameHalfStats
    - PlayerGameStats
    - PlayerGameQuarterStats
    - PlayerGameHalfStats
- establish team br_id home and away in init
- refactor pbp (see below)
- game teams stats
- game players stats

PHASE 1--REFACTOR (play by play stuff only)
+ playactions.players => playactions.player
- set feet to Plays not PlayActions
- adjust code to feed all db columns to playactions in contandum w/ appropriate python objects
    - (db) player_br_id
    - (object) Player
    
    - (db) team_br_id
    - (object) Team
    
    - (db) play_id
    
    - (db) action_code
    - (object) action: ActionMap
    
- do same for Plays
    - ...
"""
# from common import DB
import sys, os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from PlayAction import PlayAction
from ActionMap import ActionMap
from Play import Play
from PlayByPlays.GamePlayer import GamePlayer
from PlayByPlays.Team import Team
import pyperclip
import traceback

sys.path.append("..")
# from common import *


class PlayNotYetSupportedError(Exception):
    def __str__(self):
        return "This play is not yet recognized"


class Game:

    def __init__(self, br_id=None, url=None):
        if br_id:
            self.br_id = br_id
        elif url:
            self.br_id = url.split("/")[-1].replace(".html", "")
            
        self.init_plays()


    def init_plays(self):
        """
        Generate Plays with their PlayActions, associating them properly to the
        game, teams, and players
        """

        # TODO check if game exists in db, get from db if so
        url = (
            "https://www.basketball-reference.com/boxscores/pbp/" + self.br_id + ".html"
        )
        self.datetime = None
        if url.startswith("https"):
            # html in website
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
        else:
            # html in file
            with open(url, "r") as f:
                soup = f.read()

        self.soup = soup  # for debugging purposes

        table_play_by_play = soup.find("table")

        ##############################################################
        # Get the teams
        ##############################################################
        self.away_team = Team(
            name=table_play_by_play.select(".thead")[1].contents[3].text
        )
        self.home_team = Team(
            name=table_play_by_play.select(".thead")[1].contents[11].text
        )

        ##############################################################
        # Get the players
        ##############################################################
        boxscore_url = url.replace(r"pbp/", "")
        boxscore_soup = BeautifulSoup(requests.get(boxscore_url).text, "html.parser")
        away_table1 = boxscore_soup.find_all("table")[0]
        self.away_players = []
        for player_th in away_table1.find_all("th", {"class": "left"}):
            if "data-append-csv" in player_th.attrs:
                self.away_players.append(player_th["data-append-csv"])

        home_table1 = boxscore_soup.find_all("table")[8]
        self.home_players = []
        for player_th in home_table1.find_all("th", {"class": "left"}):
            if "data-append-csv" in player_th.attrs:
                self.home_players.append(player_th["data-append-csv"])

        ##############################################################
        # Get the plays
        ##############################################################
        self.plays = []
        rows = table_play_by_play.find_all("tr")
        time_index = 0
        away_index = 1
        jumpball_index = 1
        plus_points_away_index = 2
        score_index = 3
        plus_points_home_index = 4
        home_index = 5
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
                            if "Jump ball" in tds[jumpball_index].text:
                                player_jump1 = GamePlayer(
                                    url_or_br_id=tds[jumpball_index].contents[1]["href"]
                                )
                                player_jump2 = GamePlayer(
                                    url_or_br_id=tds[jumpball_index].contents[3]["href"]
                                )

                                # Jump ball
                                jump_action = PlayAction(
                                    PlayAction.JUMP_BALL, player_jump1
                                )
                                jump_action = PlayAction(
                                    PlayAction.JUMP_BALL, player_jump2
                                )

                                player_gains_posession = GamePlayer(
                                    url_or_br_id=tds[jumpball_index].contents[5]["href"]
                                )
                                gains_posession_action = PlayAction(
                                    PlayAction.GAIN_POSSESION_JUMP_BALL,
                                    player_gains_posession,
                                )
                                if (
                                    current_quarter == 1
                                    and tds[time_index].text == "12:00.0"
                                ):
                                    score = "0-0"
                                else:
                                    score = None  # ~ don't yet have a way to get score from a jumpball play
                                self.plays.append(
                                    Play(
                                        PlayActions=[
                                            jump_action,
                                            gains_posession_action,
                                        ],
                                        quarter=current_quarter,
                                        time=tds[time_index].text,
                                        score=score,
                                        distance_feet=feet,
                                    )
                                )

                            elif (
                                tds[away_index].text != "\xa0"
                                or tds[home_index].text != "\xa0"
                            ):  # If there is play-by-play content shown in the home or away columns
                                # If the content is displayed at the away side of the table
                                if tds[away_index].text != "\xa0":
                                    contents = tds[away_index].contents
                                    current_team = self.away_team
                                else:
                                    contents = tds[home_index].contents
                                    current_team = self.home_team

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
                                            team=current_team,
                                        )

                                    # INSTANT_REPLY_RULING_STANDS
                                    elif (
                                        "Instant Replay" in contents[0]
                                        and "Ruling Stands" in contents[0]
                                    ):
                                        actions = PlayAction(
                                            action=PlayAction.INSTANT_REPLY_RULING_STANDS,
                                            team=current_team,
                                        )

                                    # INSTANT_REPLY_RULING_STANDS
                                    elif "Instant Replay" in contents[0]:
                                        actions = PlayAction(
                                            action=PlayAction.INSTANT_REPLY,
                                            team=current_team,
                                        )

                                    # KICK_BALL
                                    elif "kicked ball" in contents[0]:
                                        actions = PlayAction(
                                            action=PlayAction.KICK_BALL,
                                            team=current_team,
                                        )

                                    # FULL_TIMEOUT
                                    elif "full timeout" in contents[0]:
                                        actions = PlayAction(
                                            action=PlayAction.FULL_TIMEOUT,
                                            team=current_team,
                                        )

                                    # OFFENSIVE_REBOUND_BY_TEAM
                                    elif (
                                        "Offensive rebound by Team" in contents[0]
                                        and "Team" in contents[0]
                                    ):
                                        actions = PlayAction(
                                            action=PlayAction.OFFENSIVE_REBOUND_BY_TEAM,
                                            team=current_team,
                                        )

                                    # TURNOVER_SHOT_CLOCK_VIOLATION
                                    elif (
                                        "Turnover by Team (shot clock)" in contents[0]
                                        and "Team" in contents[0]
                                    ):
                                        actions = PlayAction(
                                            action=PlayAction.TURNOVER_SHOT_CLOCK_VIOLATION,
                                            team=current_team,
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
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )

                                    # DUNK_MAKE
                                    elif "makes 2-pt dunk" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.DUNK_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # DUNK_MISS
                                    elif "misses 2-pt dunk" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.DUNK_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # FREE_THROW_MAKE
                                    elif (
                                        "makes free throw" in contents[1]
                                        or "makes flagrant free throw" in contents[1]
                                    ):
                                        actions = PlayAction(
                                            action=PlayAction.FREE_THROW_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                    # FREE_THROW_MISS
                                    elif "misses free throw" in contents[1]:
                                        actions = PlayAction(
                                            action=PlayAction.FREE_THROW_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # LAYUP_MAKE
                                    elif "makes 2-pt layup" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.LAYUP_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # LAYUP_MISS
                                    elif "misses 2-pt layup" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.LAYUP_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # HOOK_SHOT_MAKE
                                    elif "makes 2-pt hook shot" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.HOOK_SHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # HOOK_SHOT_MISS
                                    elif "misses 2-pt hook shot" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        actions = PlayAction(
                                            action=PlayAction.HOOK_SHOT_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # OFFENSIVE_REBOUND
                                    elif "Offensive rebound by " in contents[0]:
                                        actions = PlayAction(
                                            action=PlayAction.OFFENSIVE_REBOUND,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )

                                    # THREE_POINT_JUMPSHOT_MAKE
                                    elif "makes 3-pt jump shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        actions = PlayAction(
                                            action=PlayAction.THREE_POINT_JUMPSHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # THREE_POINT_JUMPSHOT_MISS
                                    elif "misses 3-pt jump shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        actions = PlayAction(
                                            action=PlayAction.THREE_POINT_JUMPSHOT_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # TWO_POINT_JUMPSHOT_MAKE
                                    elif "makes 2-pt jump shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        actions = PlayAction(
                                            action=PlayAction.TWO_POINT_JUMPSHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )

                                    # TWO_POINT_JUMPSHOT_MISS
                                    elif "misses 2-pt jump shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        actions = PlayAction(
                                            action=PlayAction.TWO_POINT_JUMPSHOT_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                    else:
                                        raise PlayNotYetSupportedError()

                                elif len(contents) == 3:
                                    # LEAVE_THE_GAME / ENTER_THE_GAME
                                    if "enters the game for" in contents[1]:
                                        leave_action = PlayAction(
                                            action=PlayAction.LEAVE_THE_GAME,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        enter_action = PlayAction(
                                            action=PlayAction.ENTER_THE_GAME,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [leave_action, enter_action]

                                    # TURNOVER_BAD_PASS
                                    elif "Turnover by" in contents[0]:
                                        actions = PlayAction(
                                            action=PlayAction.TURNOVER_BAD_PASS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
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
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        dunk_action = PlayAction(
                                            action=PlayAction.DUNK_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        assist_action = PlayAction(
                                            action=PlayAction.ASSIST,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [dunk_action, assist_action]

                                    # LAYUP_MISS / BLOCK
                                    elif "misses 2-pt layup" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        miss_action = PlayAction(
                                            action=PlayAction.LAYUP_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        block_action = PlayAction(
                                            action=PlayAction.BLOCK,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [miss_action, block_action]

                                    # LAYUP_MISS / BLOCK
                                    elif "misses 2-pt dunk" in contents[1]:
                                        if "at rim" in contents[1]:
                                            feet = 0
                                        else:
                                            feet = int(
                                                re.match(
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        miss_action = PlayAction(
                                            action=PlayAction.DUNK_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        block_action = PlayAction(
                                            action=PlayAction.BLOCK,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
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
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        layup_action = PlayAction(
                                            action=PlayAction.LAYUP_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        assist_action = PlayAction(
                                            action=PlayAction.ASSIST,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
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
                                                    ".* from (\d+) ft.*", contents[1]
                                                ).groups(1)[0]
                                            )
                                        layup_action = PlayAction(
                                            action=PlayAction.HOOK_SHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        assist_action = PlayAction(
                                            action=PlayAction.ASSIST,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [layup_action, assist_action]

                                    # THREE_POINT_JUMPSHOT_MAKE / ASSIST
                                    elif (
                                        "makes 3-pt jump shot" in contents[1]
                                        and "assist by" in contents[1]
                                    ):
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        three_point_make_action = PlayAction(
                                            action=PlayAction.THREE_POINT_JUMPSHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        assist_action = PlayAction(
                                            action=PlayAction.ASSIST,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
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
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        three_point_make_action = PlayAction(
                                            action=PlayAction.TWO_POINT_JUMPSHOT_MAKE,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        assist_action = PlayAction(
                                            action=PlayAction.ASSIST,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [
                                            three_point_make_action,
                                            assist_action,
                                        ]

                                    # TWO_POINT_JUMPSHOT_MISS / BLOCK
                                    elif "misses 2-pt jump shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        miss_action = PlayAction(
                                            action=PlayAction.TWO_POINT_JUMPSHOT_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        block_action = PlayAction(
                                            action=PlayAction.BLOCK,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [miss_action, block_action]

                                    # HOOK_SHOT_MISS / BLOCK
                                    elif "misses 2-pt hook shot" in contents[1]:
                                        feet = int(
                                            re.match(
                                                ".* from (\d+) ft.*", contents[1]
                                            ).groups(1)[0]
                                        )
                                        miss_action = PlayAction(
                                            action=PlayAction.HOOK_SHOT_MISS,
                                            player=GamePlayer(
                                                url_or_br_id=contents[0]["href"]
                                            ),
                                        )
                                        block_action = PlayAction(
                                            action=PlayAction.BLOCK,
                                            player=GamePlayer(
                                                url_or_br_id=contents[2]["href"]
                                            ),
                                        )
                                        actions = [miss_action, block_action]
                                    else:
                                        raise PlayNotYetSupportedError()
                                elif len(contents) == 5:
                                    # BLOCKING_FOUL_COMMIT / BLOCKING_FOUL_DRAW
                                    if "Shooting foul by" in contents[0]:
                                        commit_foul_action = PlayAction(
                                            action=PlayAction.BLOCKING_FOUL_COMMIT,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )
                                        draw_foul_action = PlayAction(
                                            action=PlayAction.BLOCKING_FOUL_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )
                                        actions = [commit_foul_action, draw_foul_action]

                                    # LOOSE_BALL_FOUL_COMMIT / LOOSE_BALL_FOUL_DRAW
                                    elif "Loose ball foul by" in contents[0]:
                                        commit_foul_action = PlayAction(
                                            action=PlayAction.LOOSE_BALL_FOUL_COMMIT,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )
                                        draw_foul_action = PlayAction(
                                            action=PlayAction.LOOSE_BALL_FOUL_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )
                                        actions = [commit_foul_action, draw_foul_action]

                                    # OFFENSIVE_FOUL_COMMIT / STEAL
                                    elif (
                                        "Offensive foul by" in contents[0]
                                        and "drawn by" in contents[2]
                                    ):
                                        offensive_commit_action = PlayAction(
                                            action=PlayAction.OFFENSIVE_FOUL_COMMIT,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )

                                        offensive_draw_action = PlayAction(
                                            action=PlayAction.OFFENSIVE_FOUL_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
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
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )
                                        draw_foul_action = PlayAction(
                                            action=PlayAction.PERSONAL_FOUL_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )
                                        actions = [commit_foul_action, draw_foul_action]

                                    # SHOOTING_FOUL_COMMIT / SHOOTING_FOUL_DRAW
                                    elif "Shooting foul by" in contents[0]:
                                        commit_foul_action = PlayAction(
                                            action=PlayAction.SHOOTING_FOUL_COMMIT,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )
                                        draw_foul_action = PlayAction(
                                            action=PlayAction.SHOOTING_FOUL_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )
                                        actions = [commit_foul_action, draw_foul_action]

                                    # TURNOVER_BAD_PASS / STEAL
                                    elif (
                                        "Turnover by" in contents[0]
                                        and "bad pass; steal by" in contents[2]
                                    ):
                                        player_turnover = GamePlayer(
                                            url_or_br_id=contents[1]["href"]
                                        )
                                        turnover_action = PlayAction(
                                            action=PlayAction.TURNOVER_BAD_PASS,
                                            player=player_turnover,
                                        )

                                        player_steal = GamePlayer(
                                            url_or_br_id=contents[3]["href"]
                                        )
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
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )

                                        steal_action = PlayAction(
                                            action=PlayAction.STEAL,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )

                                        actions = [turnover_action, steal_action]
                                    # FLAGRANT_FOUL_TYPE_1 / FLAGRANT_FOUL_TYPE_1_DRAW
                                    elif "Flagrant foul type 1 by" in contents[0]:
                                        commit_foul_action = PlayAction(
                                            action=PlayAction.FLAGRANT_FOUL_TYPE_1,
                                            player=GamePlayer(
                                                url_or_br_id=contents[1]["href"]
                                            ),
                                        )
                                        draw_foul_action = PlayAction(
                                            action=PlayAction.FLAGRANT_FOUL_TYPE_1_DRAW,
                                            player=GamePlayer(
                                                url_or_br_id=contents[3]["href"]
                                            ),
                                        )
                                        actions = [commit_foul_action, draw_foul_action]
                                    else:
                                        raise PlayNotYetSupportedError()
                                else:
                                    raise PlayNotYetSupportedError()

                                self.plays.append(
                                    Play(
                                        PlayActions=actions,
                                        quarter=current_quarter,
                                        time=tds[time_index].text,
                                        score=tds[score_index].text,
                                        distance_feet=feet,
                                    )
                                )
                            else:
                                raise PlayNotYetSupportedError()
                        except PlayNotYetSupportedError as e:
                            import traceback

                            quarter = current_quarter
                            time = tds[time_index]
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
                            
                            if input("Save new action map entry before coding a new if check? (y/n)").strip().lower() == "y":
                                code = input('REQUIRED: action map code: ').strip()
                                description = input('OPTIONAL: action map description: ').strip()
                                ActionMap.save_new(code=code, description=description)
                                raise Exception("New action map entry saved. Please code a new if check for this play.")
                            
                        except Exception as e:
                            import traceback

                            quarter = current_quarter
                            time = tds[time_index]
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


    def set_player_game_stats_ALL_QUARTERS(self):
        """
        set_player_game_stats initializing and setting all data for
        PlayerGameQuarterStats and PlayerGameHalfStats for all quarters and
        halves
        """
        try:
            pass
        except Exception as e:
            print("ERROR SETTING PLAYERS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def flush_player_game_stats_ALL_QUARTERS(self):
        """
        flush_player_game_stats for each quarter and half to db
        """
        try:
            pass
        except Exception as e:
            print("ERROR SAVING PLAYERS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def set_team_game_stats(self):
        """
        set_team_game_stats initializing and setting all data for TeamGameStats
        """
        try:
            pass
        except Exception as e:
            print("ERROR SETTING TEAMS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def flush_team_game_stats(self):
        """
        flush_team_game_stats to db
        """
        try:
            pass
        except Exception as e:
            print("ERROR SAVING TEAMS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def set_team_game_stats_ALL_QUARTERS(self):
        """
        set_team_game_stats initializing and setting all data for
        TeamGameQuarterStats and TeamGameHalfStats for all quarters and halves
        """
        try:
            pass
        except Exception as e:
            print("ERROR SETTING TEAMS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def flush_team_game_stats_ALL_QUARTERS(self):
        """
        flush_team_game_stats for each quarter and half to db
        """
        try:
            pass
        except Exception as e:
            print("ERROR SAVING TEAMS--", e)
            print("BR_ID: " + self.br_id)
            print(traceback.format_exc())
            breakpoint()
            breakpoint()


    def __str__(self):
        play_str_list = []
        for play in self.plays:
            play_str_list.append(
                "Q" + str(play.quarter) + " " + play.time + "\n" + str(play)
            )

        return "\n\n".join(play_str_list)


    def __iter__(self):
        # Build the data to save
        for play in self.plays:
            row_builder = {}
            row_builder["Quarter"] = "Q" + str(play.quarter)
            row_builder["Time"] = play.time
            row_builder["Actions"] = " | ".join(list(play))
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
            row_builder["Quarter"] = "Q" + str(play.quarter)
            row_builder["Time"] = play.time
            row_builder["Actions"] = " | ".join(list(play))
            excel_builder.append(row_builder)

        # Save the data
        pd.DataFrame(excel_builder).to_excel("game.xlsx", index=False)

        # Open the file with excel
        os.startfile("game.xlsx")
