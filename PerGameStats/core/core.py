r"""TODO
- all pgs,pgqs,pghs due to team_br_id problem
    -/ json
    - db
- import OT for all tables
- 1980 html missing last several games-- impacts pgs,tgs
- download pbp html
- PerGameStats/corrections/202008150POR
  - manual user input bc its unavailable
"""

# region IMPORTS and CONFIG
import json
import pandas as pd
import bs4
import traceback
import numpy as np
import TeamGameStats
import os
import re
import pyperclip
import TeamGameStats.helper
import TeamGameHalfStats.helper
import TeamGameQuarterStats.helper
import PlayerGameStats.helper
import PlayerGameHalfStats.helper
import PlayerGameQuarterStats.helper
from core.helper import *
import warnings
from sqlalchemy import text

# from sqlalchemy.exc import RemovedIn20Warning
warnings.filterwarnings("ignore", category=UserWarning)
# warnings.filterwarnings("ignore", category=RemovedIn20Warning)
import duckdb

# endregion


def getTeamGameStatsHTML(
    start_year: int | None = None,
    stop_year: int = 1946,
    singular_game_br_id: str | None = None,
    override_existing_html: bool = False,
) -> None:
    """
    Download—or rebuild—box-score HTML files and save them under ``html/<year>/``.

    The function works in **one of two modes**:

    1. **Bulk mode** (default)
       Loop backward from ``start_year`` down to ``stop_year`` and save every
       game's HTML—skipping files that already exist.

    2. **Single-game mode**
       Provide ``singular_game_br_id`` (e.g., ``"20250328LAL"``) to process just
       that one game, ignoring all other arguments.

    Parameters
    ----------
    start_year : int, optional
        First NBA season to process (e.g., ``2025`` for the 2025-26 season).
        Defaults to the current calendar year if *None*.  Ignored in single-game
        mode.
    stop_year : int, default ``1946``
        Last season to process (inclusive) when looping in bulk mode.
    singular_game_br_id : str, optional
        A Basketball-Reference game ID.  When supplied, the function switches to
        single-game mode.
    override_existing_html : bool, default ``False``
        Overwrite any existing HTML instead of resuming.  You’ll be prompted to
        confirm with ``y`` at runtime.

    Returns
    -------
    None
        The function performs its work via file writes and console output.

    Examples
    --------
    >>> # Resume bulk download from 2025 down to 1946
    >>> getTeamGameStatsHTML(start_year=2025)
    >>> # Rebuild a single game
    >>> getTeamGameStatsHTML(singular_game_br_id="202401151OKC")
    """

    if override_existing_html:
        if (
            input(
                'THIS IS OVERRIDING EXISTING HTML RATHER THAN PICKING UP WHERE THE SCRIPT LEFT OFF.\nInput "y" to continue:'
            )
            == "y"
        ):
            print("Proceeding script...")
        else:
            print(
                "Set override_existing_html to False (or omit the argument) in the call to getTeamGameStatsHTML"
            )

    if singular_game_br_id:
        season_year = get_season_from_br_id(singular_game_br_id)
        SQL = f"""SELECT * FROM Games
        where br_id = '{singular_game_br_id}'"""
        game = pd.read_sql(sql=SQL, con=engine)
        if not game.empty:
            game = game.iloc[0]
            save_html(game, season_year)
            return
        else:
            print(f"Game {singular_game_br_id} not found in the database")
            return

    else:
        start_year = int(start_year)
        stop_year = int(stop_year)

        year = start_year
        while year >= stop_year:
            SQL = f"""SELECT * FROM Games 
            where date_time >= '{year}-09-01'
            and date_time < '{year + 1}-09-01'
            order by date_time desc"""

            games = pd.read_sql(sql=SQL, con=engine)

            # Catch up to where we left off
            left_off_game_br_id = None
            for folder in os.listdir("html"):
                if folder.isnumeric() and int(folder) > year:
                    continue
                elif folder == ".gitkeep":
                    continue
                else:
                    # If contents in folder
                    if os.listdir(f"html/{folder}"):
                        # Get the last file ascending
                        files = os.listdir(f"html/{folder}")
                        files.sort()
                        last_file = files[0]
                        left_off_game_br_id = last_file.split("-")[1].split(".")[0]

            for ind, game in games.iterrows():
                if not override_existing_html:
                    if left_off_game_br_id:
                        # Pick up where we left off if we have to
                        if left_off_game_br_id == game["br_id"]:
                            # Skip to the next game
                            if left_off_game_br_id:
                                left_off_game_br_id = False
                        continue

                with open("lastgamehtml.txt", "w") as f:
                    f.write(game.br_id)
                save_html(game, year)

                print("SAVED")
            print("YEAR " + str(year) + " COMPLETE")
            year -= 1
    print("EXITED")


def setTeamGameStatsJSON(
    begin_year=None,
    stop_year=1946,
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
):

    begin_year = int(begin_year)
    stop_year = int(stop_year)

    year = begin_year

    # Get the latest game data processed. The script will have left off at the game furthest in the past
    game_leftoff_at = get_last_processed_game("TeamGameStats")
    game_quarter_leftoff_at = get_last_processed_game("TeamGameQuarterStats")
    game_half_leftoff_at = get_last_processed_game("TeamGameHalfStats")

    while year >= stop_year:
        # DB Games
        SQL = f"""SELECT * FROM Games 
                where date_time >= '{year}-09-01'
                and date_time < '{year + 1}-09-01'
                order by date_time desc"""

        try:
            games = pd.read_sql(sql=SQL, con=engine)
        except Exception as e:
            print("----------------")
            print("ERROR GETTING GAME FROM DB!: " + str(e) + "\n")
            traceback.print_exc()
            print("\nGame details:")
            print(games)
            print("----------------")
            breakpoint()

        for file in os.listdir(f"html/{year}"):

            if file.endswith(".html"):

                # region DATA PREP
                game = games[games["br_id"] == file.split("-")[1].split(".")[0]].iloc[0]

                # What should we skip, if at all?
                skip_TeamGameStats = is_game_processed(game.br_id, game_leftoff_at)
                skip_TeamGameQuarterStats = is_game_processed(
                    game.br_id, game_quarter_leftoff_at
                )
                skip_TeamGameHalfStats = is_game_processed(
                    game.br_id, game_half_leftoff_at
                )

                # If data should be skipped for all specified tables, continue to the next file
                if (
                    (get_TeamGameStats == False or skip_TeamGameStats)
                    and (get_TeamGameQuarterStats == False or skip_TeamGameQuarterStats)
                    and (get_TeamGameHalfStats == False or skip_TeamGameHalfStats)
                ):
                    continue

                print(file)

                with open(f"html/{year}/{file}", "r", encoding="utf-8") as f:
                    html = f.read()

                soup = bs4.BeautifulSoup(html, "html.parser")

                four_factors = get_tag_having_text(soup, "table", "Four Factors Table")

                if len(soup.select("#inactive_players")) > 0:
                    inactive_players = soup.select("#inactive_players")[0]
                else:
                    inactive_players = None
                home_team_br_id = remove_numbers(game.br_id)
                away_team_br_id = soup.select(".stats_table")[0]["id"].split("-")[1]

                away_team_basic = soup.select(f"#box-{away_team_br_id}-game-basic")[0]
                home_team_basic = soup.select(f"#box-{home_team_br_id}-game-basic")[0]

                try:
                    away_team_advanced = soup.select(
                        f"#box-{away_team_br_id}-game-advanced"
                    )[0]
                except IndexError:
                    away_team_advanced = None

                try:
                    home_team_advanced = soup.select(
                        f"#box-{home_team_br_id}-game-advanced"
                    )[0]
                except IndexError:
                    home_team_advanced = None

                # region GET QUARTER AND HALF STATS HTML
                if year > 1995:
                    home_team_q1 = soup.select(f"#box-{home_team_br_id}-q1-basic")[0]
                    home_team_q2 = soup.select(f"#box-{home_team_br_id}-q2-basic")[0]
                    home_team_q3 = soup.select(f"#box-{home_team_br_id}-q3-basic")[0]
                    home_team_q4 = soup.select(f"#box-{home_team_br_id}-q4-basic")[0]
                    away_team_q1 = soup.select(f"#box-{away_team_br_id}-q1-basic")[0]
                    away_team_q2 = soup.select(f"#box-{away_team_br_id}-q2-basic")[0]
                    away_team_q3 = soup.select(f"#box-{away_team_br_id}-q3-basic")[0]
                    away_team_q4 = soup.select(f"#box-{away_team_br_id}-q4-basic")[0]
                    home_team_h1 = soup.select(f"#box-{home_team_br_id}-h1-basic")[0]
                    home_team_h2 = soup.select(f"#box-{home_team_br_id}-h2-basic")[0]
                    away_team_h1 = soup.select(f"#box-{away_team_br_id}-h1-basic")[0]
                    away_team_h2 = soup.select(f"#box-{away_team_br_id}-h2-basic")[0]

                else:
                    home_team_q1 = None
                    home_team_q2 = None
                    home_team_q3 = None
                    home_team_q4 = None
                    away_team_q1 = None
                    away_team_q2 = None
                    away_team_q3 = None
                    away_team_q4 = None
                    home_team_h1 = None
                    home_team_h2 = None
                    away_team_h1 = None
                    away_team_h2 = None
                # endregion
                next_field = ""
                # endregion

                try:

                    # region DATA SAVING
                    if get_TeamGameStats and not skip_TeamGameStats:

                        home_tgs = {}
                        away_tgs = {}

                        TeamGameStats.helper.setJSON(
                            games,
                            away_team_basic,
                            home_team_basic,
                            four_factors,
                            inactive_players,
                            away_team_advanced,
                            home_team_advanced,
                            home_tgs,
                            away_tgs,
                            file,
                            year,
                        )

                        data = [away_tgs, home_tgs]

                        insertDataJL(
                            f"TeamGameStats/json/{year}TeamGameStats.jsonl",
                            new_data=data,
                        )

                    if get_TeamGameQuarterStats and not skip_TeamGameQuarterStats:

                        home_tgs1 = {}
                        away_tgs1 = {}
                        home_tgs2 = {}
                        away_tgs2 = {}
                        home_tgs3 = {}
                        away_tgs3 = {}
                        home_tgs4 = {}
                        away_tgs4 = {}

                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q1,
                            home_team_q1,
                            four_factors,
                            home_tgs1,
                            away_tgs1,
                            1,
                            file,
                            year,
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q2,
                            home_team_q2,
                            four_factors,
                            home_tgs2,
                            away_tgs2,
                            2,
                            file,
                            year,
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q3,
                            home_team_q3,
                            four_factors,
                            home_tgs3,
                            away_tgs3,
                            3,
                            file,
                            year,
                        )
                        TeamGameQuarterStats.helper.setJSON(
                            games,
                            away_team_q4,
                            home_team_q4,
                            four_factors,
                            home_tgs4,
                            away_tgs4,
                            4,
                            file,
                            year,
                        )

                        data = [
                            away_tgs1,
                            home_tgs1,
                            away_tgs2,
                            home_tgs2,
                            away_tgs3,
                            home_tgs3,
                            away_tgs4,
                            home_tgs4,
                        ]

                        insertDataJL(
                            f"TeamGameQuarterStats/json/{year}TeamGameQuarterStats.jsonl",
                            new_data=data,
                        )

                    if get_TeamGameHalfStats and not skip_TeamGameHalfStats:

                        home_tgs1 = {}
                        away_tgs1 = {}
                        home_tgs2 = {}
                        away_tgs2 = {}

                        TeamGameHalfStats.helper.setJSON(
                            games,
                            away_team_h1,
                            home_team_h1,
                            four_factors,
                            home_tgs1,
                            away_tgs1,
                            1,
                            file,
                            year,
                        )
                        TeamGameHalfStats.helper.setJSON(
                            games,
                            away_team_h2,
                            home_team_h2,
                            four_factors,
                            home_tgs2,
                            away_tgs2,
                            2,
                            file,
                            year,
                        )

                        data = [
                            away_tgs1,
                            home_tgs1,
                            away_tgs2,
                            home_tgs2,
                        ]

                        insertDataJL(
                            f"TeamGameHalfStats/json/{year}TeamGameHalfStats.jsonl",
                            new_data=data,
                        )
                    # endregion

                except Exception as e:
                    print("----------------")
                    print(f"ERROR getting {next_field}: " + str(e) + "\n")
                    traceback.print_exc()
                    print("----------------")
                    breakpoint()

        year -= 1


def setPlayerGameStatsJSON(
    begin_year,
    stop_year=1946,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
    testQL: str | None = None,
):
    """
    :param testQL: str - SQL for one off testing rather than all games in the
        years range. Outputs to jl files with Test in the name
    """
    begin_year = int(begin_year)
    stop_year = int(stop_year)

    year = begin_year

    # Get the latest game data processed. The script will have left off at the game furthest in the past
    game_leftoff_at = get_last_processed_game("PlayerGameStats")
    game_quarter_leftoff_at = get_last_processed_game("PlayerGameQuarterStats")
    game_half_leftoff_at = get_last_processed_game("PlayerGameHalfStats")

    while year >= stop_year:
        # DB Games
        SQL = f"""SELECT * FROM Games 
                where date_time >= '{year}-09-01'
                and date_time < '{year + 1}-09-01'
                order by date_time desc"""

        try:
            games = pd.read_sql(sql=SQL, con=engine)
        except Exception as e:
            print("----------------")
            print("ERROR GETTING GAME FROM DB!: " + str(e) + "\n")
            traceback.print_exc()
            print("\nGame details:")
            print(games)
            print("----------------")
            breakpoint()

        new_data = []
        for file in os.listdir(f"html/{year}"):
            if file.endswith(".html"):

                try:
                    # region DATA PREP
                    game = games[games["br_id"] == file.split("-")[1].split(".")[0]]
                    if game.empty and testQL:
                        continue
                    game = game.iloc[0]

                    if testQL:
                        # Not skipping, testing everything in the testQL query
                        skip_PlayerGameStats = False
                        skip_PlayerGameQuarterStats = False
                        skip_PlayerGameHalfStats = False
                    else:
                        # What should we skip, if at all?
                        skip_PlayerGameStats = is_game_processed(
                            game.br_id, game_leftoff_at
                        )
                        skip_PlayerGameQuarterStats = is_game_processed(
                            game.br_id, game_quarter_leftoff_at
                        )
                        skip_PlayerGameHalfStats = is_game_processed(
                            game.br_id, game_half_leftoff_at
                        )

                        # If data should be skipped for all specified tables, continue to the next file
                        if (
                            (get_PlayerGameStats == False or skip_PlayerGameStats)
                            and (
                                get_PlayerGameQuarterStats == False
                                or skip_PlayerGameQuarterStats
                            )
                            and (
                                get_PlayerGameHalfStats == False
                                or skip_PlayerGameHalfStats
                            )
                        ):
                            continue

                    print(file)

                    with open(f"html/{year}/{file}", "r", encoding="utf-8") as f:
                        html = f.read()

                    soup = bs4.BeautifulSoup(html, "html.parser")

                    four_factors = get_tag_having_text(
                        soup, "table", "Four Factors Table"
                    )

                    if len(soup.select("#inactive_players")) > 0:
                        inactive_players = soup.select("#inactive_players")[0]

                    home_team_br_id = remove_numbers(game.br_id)
                    away_team_br_id = soup.select(".stats_table")[0]["id"].split("-")[1]

                    away_team_basic = soup.select(f"#box-{away_team_br_id}-game-basic")[
                        0
                    ]
                    home_team_basic = soup.select(f"#box-{home_team_br_id}-game-basic")[
                        0
                    ]
                    try:
                        away_team_advanced = soup.select(
                            f"#box-{away_team_br_id}-game-advanced"
                        )[0]
                    except IndexError:
                        away_team_advanced = None

                    try:
                        home_team_advanced = soup.select(
                            f"#box-{home_team_br_id}-game-advanced"
                        )[0]
                    except IndexError:
                        home_team_advanced = None

                    # region GET QUARTER AND HALF STATS HTML
                    if year > 1995:

                        home_team_q1 = soup.select(f"#box-{home_team_br_id}-q1-basic")[
                            0
                        ]
                        home_team_q2 = soup.select(f"#box-{home_team_br_id}-q2-basic")[
                            0
                        ]
                        home_team_q3 = soup.select(f"#box-{home_team_br_id}-q3-basic")[
                            0
                        ]
                        home_team_q4 = soup.select(f"#box-{home_team_br_id}-q4-basic")[
                            0
                        ]
                        away_team_q1 = soup.select(f"#box-{away_team_br_id}-q1-basic")[
                            0
                        ]
                        away_team_q2 = soup.select(f"#box-{away_team_br_id}-q2-basic")[
                            0
                        ]
                        away_team_q3 = soup.select(f"#box-{away_team_br_id}-q3-basic")[
                            0
                        ]
                        away_team_q4 = soup.select(f"#box-{away_team_br_id}-q4-basic")[
                            0
                        ]
                        home_team_h1 = soup.select(f"#box-{home_team_br_id}-h1-basic")[
                            0
                        ]
                        home_team_h2 = soup.select(f"#box-{home_team_br_id}-h2-basic")[
                            0
                        ]
                        away_team_h1 = soup.select(f"#box-{away_team_br_id}-h1-basic")[
                            0
                        ]
                        away_team_h2 = soup.select(f"#box-{away_team_br_id}-h2-basic")[
                            0
                        ]
                    else:
                        home_team_q1 = None
                        home_team_q2 = None
                        home_team_q3 = None
                        home_team_q4 = None
                        away_team_q1 = None
                        away_team_q2 = None
                        away_team_q3 = None
                        away_team_q4 = None
                        home_team_h1 = None
                        home_team_h2 = None
                        away_team_h1 = None
                        away_team_h2 = None
                    # endregion

                    next_field = ""
                    # endregion
                    try:

                        # region DATA SAVING
                        if get_PlayerGameStats and not skip_PlayerGameStats:
                            home_tgs = {}
                            away_tgs = {}

                            new_data += PlayerGameStats.helper.setJSON(
                                game,
                                away_team_basic,
                                home_team_basic,
                                four_factors,
                                away_team_advanced,
                                home_team_advanced,
                            )
                            if testQL:
                                insertDataJL(
                                    f"PlayerGameStats/json/TestPlayerGameStats.jsonl",
                                    new_data=new_data,
                                )
                            else:
                                insertDataJL(
                                    f"PlayerGameStats/json/{year}PlayerGameStats.jsonl",
                                    new_data=new_data,
                                )
                            new_data = []

                        if (
                            get_PlayerGameQuarterStats
                            and not skip_PlayerGameQuarterStats
                        ):
                            if year > 1995:
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    1,
                                    home_team_q1,
                                    away_team_q1,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    2,
                                    home_team_q2,
                                    away_team_q2,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    3,
                                    home_team_q3,
                                    away_team_q3,
                                    four_factors,
                                )
                                new_data += PlayerGameQuarterStats.helper.setJSON(
                                    game,
                                    4,
                                    home_team_q4,
                                    away_team_q4,
                                    four_factors,
                                )

                                if testQL:
                                    insertDataJL(
                                        f"PlayerGameQuarterStats/json/TestPlayerGameQuarterStats.jsonl",
                                        new_data=new_data,
                                    )
                                else:
                                    insertDataJL(
                                        f"PlayerGameQuarterStats/json/{year}PlayerGameQuarterStats.jsonl",
                                        new_data=new_data,
                                    )
                                new_data = []

                        if get_PlayerGameHalfStats and not skip_PlayerGameHalfStats:
                            if year > 1995:
                                home_tgs1 = {}
                                away_tgs1 = {}
                                home_tgs2 = {}
                                away_tgs2 = {}
                                new_data += PlayerGameHalfStats.helper.setJSON(
                                    game,
                                    1,
                                    away_team_h1,
                                    home_team_h1,
                                    four_factors,
                                )
                                new_data += PlayerGameHalfStats.helper.setJSON(
                                    game,
                                    2,
                                    away_team_h2,
                                    home_team_h2,
                                    four_factors,
                                )

                                if testQL:
                                    insertDataJL(
                                        f"PlayerGameHalfStats/json/TestPlayerGameHalfStats.jsonl",
                                        new_data=new_data,
                                    )
                                else:
                                    insertDataJL(
                                        f"PlayerGameHalfStats/json/{year}PlayerGameHalfStats.jsonl",
                                        new_data=new_data,
                                    )
                                new_data = []
                        # endregion

                    except Exception as e:
                        print("\n----------------")
                        print(f"ERROR getting {next_field}: " + str(e) + "\n")
                        traceback.print_exc()
                        print("----------------\n")
                        breakpoint()
                except Exception as e:
                    handle_err(e, game)

        year -= 1


def lsJSON(
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
):
    """
    Process JSON files into the database reverse chronologically
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    """

    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]

    data_file_pattern = re.compile(r"\d{4}.*.jsonl")
    str_output = ""
    for table in tables:
        str_output += f"\n\n{table}:"
        for file in os.listdir(f"{table}/json"):
            if data_file_pattern.match(file):
                str_output += f"\n\t{file}"

    print(str_output)


def rmJSON(
    newest_year,
    oldest_year,
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
):
    """
    remove JSON files from the file system
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    """

    target_table_count = 0
    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]

    data_file_pattern = re.compile(r"\d{4}.*.jsonl")
    str_output = ""
    for table in tables:
        str_output += f"\n\n{table}:"
        for file in os.listdir(f"{table}/json"):
            if data_file_pattern.match(file):
                if int(file[:4]) <= newest_year and int(file[:4]) >= oldest_year:
                    str_output += f"\n\tDELETED {file}"

                    os.remove(f"{table}/json/{file}")

    print(str_output)


def lsdb(
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
):
    """
    show where progress was left off for importing data in the database
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    """
    tables = []
    if get_TeamGameStats:
        tables += ["TeamGameStats"]
    if get_TeamGameQuarterStats:
        tables += ["TeamGameQuarterStats"]
    if get_TeamGameHalfStats:
        tables += ["TeamGameHalfStats"]
    if get_PlayerGameStats:
        tables += ["PlayerGameStats"]
    if get_PlayerGameQuarterStats:
        tables += ["PlayerGameQuarterStats"]
    if get_PlayerGameHalfStats:
        tables += ["PlayerGameHalfStats"]

    basic_table_sql = ""
    advanced_table_sql = ""
    is_first_basic_table = True
    is_first_advancded_table = True
    for table in tables:
        if table.lower() in ["tgs", "pgs", "teamgamestats", "playergamestats"]:
            if is_first_basic_table:
                basic_table_sql = f"""select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}"""
            else:
                basic_table_sql += f"""\nunion select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                    union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}"""
            is_first_basic_table = False
        else:
            if is_first_advancded_table:
                advanced_table_sql = f"""select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}"""
            else:
                advanced_table_sql += f"""\nunion select "FIRST {table}" as "table", min(game_br_id) as "game_br_id" from {table}
                    union select "LAST {table}" as "table", max(game_br_id) as "game_br_id" from {table}"""
            is_first_advancded_table = False
    basic_table_sql += ";"
    with create_engine(conn_str).begin() as connection:
        basic_df = pd.read_sql(sql=basic_table_sql, con=engine)
        advanced_df = pd.read_sql(sql=advanced_table_sql, con=engine)
    print("\nBASIC DATA:")
    print(basic_df.to_string(index=False))
    print("\n\nADVANCED DATA:")
    print(advanced_df.to_string(index=False))


def loadJSONToDB(
    begin_year,
    stop_year,
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
    debug=False,
):
    """
    Process JSON files into the database reverse chronologically
    :param stop_year: int - The newest year to process
    :param begin_year: int - The oldest year to process
    :param get_TeamGameStats: bool - Load TeamGameStats
    :param get_TeamGameQuarterStats: bool - Load TeamGameQuarterStats
    :param get_TeamGameHalfStats: bool - Load TeamGameHalfStats
    :param get_PlayerGameStats: bool - Load PlayerGameStats
    :param get_PlayerGameQuarterStats: bool - Load PlayerGameQuarterStats
    :param get_PlayerGameHalfStats: bool - Load PlayerGameHalfStats
    :param debug: bool - Load data in table with '2' appended to the table name for testing purposes
    """

    ###########################################################
    def clean_data(games):

        try: 
            # Convert to boolean
            if "played" in games.columns:
                games["played"] = games["played"].astype(bool)
            if "started" in games.columns:
                games["started"] = games["started"].astype(bool)

            if get_TeamGameStats:
                games.loc[games.offensive_rebounds == "", "offensive_rebounds"] = np.nan
                games.loc[games.defensive_rebounds == "", "defensive_rebounds"] = np.nan
                games.loc[games.pace_factor == "", "pace_factor"] = np.nan
                games.loc[games.offensive_rating == "", "offensive_rating"] = np.nan
                games.loc[games.defensive_rating == "", "defensive_rating"] = np.nan
                games.loc[
                    games.offensive_rebound_percentage == "", "offensive_rebound_percentage"
                ] = np.nan
                games.loc[
                    games.defensive_rebound_percentage == "", "defensive_rebound_percentage"
                ] = np.nan
                games.loc[games.steal_percentage == "", "steal_percentage"] = np.nan
                games.loc[games.steals == "", "steals"] = np.nan
                games.loc[games.turnovers == "", "turnovers"] = np.nan
                games.loc[games.blocks == "", "blocks"] = np.nan
                games.loc[games.field_goal_attempts == "", "field_goal_attempts"] = np.nan
                games.loc[games.field_goal_percentage == "", "field_goal_percentage"] = (
                    np.nan
                )
                games.loc[games.assists == "", "assists"] = np.nan
                games.loc[games.rebounds == "", "rebounds"] = np.nan
                games.loc[games.personal_fouls == "", "personal_fouls"] = np.nan
                games.loc[games.minutes_played == "", "minutes_played"] = np.nan
                games.loc[games.ft_per_fga == "", "ft_per_fga"] = np.nan
                games.loc[games.free_throw_attempts == "", "free_throw_attempts"] = np.nan
                games.loc[games.free_throw_percentage == "", "free_throw_percentage"] = np.nan

            if get_PlayerGameStats:
                #region one-off fixes
                # if '202103270LAC' in list(games.game_br_id):
                #     # TODO this is sus
                #     games.loc[(games.game_br_id == '202103270LAC') & (games.player_br_id == 'howardw01'), 'free_throw_attempt_rate'] = .609 # no idea y

                if "201601210DEN" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "201601210DEN")
                        & (games.player_br_id == "millemi01"),
                        "box_plus_minus",
                    ] = None  # no idea y

                if "201411070ORL" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "201411070ORL")
                        & (games.player_br_id == "bennean01"),
                        "box_plus_minus",
                    ] = None  # no idea y

                # if '201412290MIA' in list(games.game_br_id):
                #     games.loc[(games.game_br_id == '201412290MIA') & (games.player_br_id == 'whiteha01'), 'free_throw_attempt_rate'] = None # no idea y

                if "201312300DEN" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "201312300DEN")
                        & (games.player_br_id == "anthojo01"),
                        "box_plus_minus",
                    ] = None  # no idea y

                if "200305250DAL" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "200305250DAL")
                        & (games.player_br_id == "kerrst01"),
                        "box_plus_minus",
                    ] = None  # no idea y

                if "200102130VAN" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "200102130VAN")
                        & (games.player_br_id == "carrch01"),
                        "box_plus_minus",
                    ] = None  # no idea y

                if "200911030DAL" in list(games.game_br_id):
                    games.loc[
                        (games.game_br_id == "200911030DAL")
                        & (games.player_br_id == "koufoko01"),
                        "box_plus_minus",
                    ] = None  # no idea y
                    games.loc[
                        (games.game_br_id == "200911030DAL")
                        & (games.player_br_id == "koufoko01"),
                        "defensive_rating",
                    ] = 0  # no idea y
                    
            #endregion

            # shift decimal two places
            def shift_decimal(val):
                if str(val) == "nan":
                    return val

                # weird quirk where the website shows %100 as %-1000
                if val == -1000:
                    return 1.0

                str_val = str(val)
                dec_pos = str(str_val).rfind(".")
                if dec_pos == 0:
                    return float(".00" + str_val.replace(".", ""))
                elif dec_pos == 1:
                    return float(".0" + str_val.replace(".", ""))
                else:
                    return float(
                        str_val[: dec_pos - 2]
                        + "."
                        + str_val[dec_pos - 2 :].replace(".", "")
                    )

            if "offensive_rebound_percentage" in games.columns:
                games["offensive_rebound_percentage"] = games[
                    "offensive_rebound_percentage"
                ].apply(shift_decimal)
            if "defensive_rebound_percentage" in games.columns:
                games["defensive_rebound_percentage"] = games[
                    "defensive_rebound_percentage"
                ].apply(shift_decimal)
            if "total_rebound_percentage" in games.columns:
                games["total_rebound_percentage"] = games["total_rebound_percentage"].apply(
                    shift_decimal
                )
            if "assist_percentage" in games.columns:
                games["assist_percentage"] = games["assist_percentage"].apply(shift_decimal)
            if "steal_percentage" in games.columns:
                games["steal_percentage"] = games["steal_percentage"].apply(shift_decimal)
            if "block_percentage" in games.columns:
                games["block_percentage"] = games["block_percentage"].apply(shift_decimal)
            if "turnover_percentage" in games.columns:
                games["turnover_percentage"] = games["turnover_percentage"].apply(
                    shift_decimal
                )
            if "usage_percentage" in games.columns:
                games["usage_percentage"] = games["usage_percentage"].apply(shift_decimal)
            if "box_plus_minus" in games.columns:
                games["box_plus_minus"] = games["box_plus_minus"].apply(
                    lambda x: None if x == -1000 else x
                )

            if "three_pointer_percentage" in games.columns:

                games.three_pointer_percentage = games.three_pointer_percentage.apply(
                    lambda val: 0 if val == ".000" else val
                )
                games.three_pointer_percentage = games.three_pointer_percentage.apply(
                    lambda val: np.nan if val == "" else val
                )

                games.free_throw_percentage = games.free_throw_percentage.apply(
                    lambda val: 0 if val == ".000" else val
                )
                games.free_throw_percentage = games.free_throw_percentage.apply(
                    lambda val: np.nan if val == "" else val
                )
            if "inactive_players" in games.columns:
                games["inactive_players"] = games["inactive_players"].apply(
                    lambda x: json.dumps(x)
                )
            if "minutes_played" in games.columns and (
                get_PlayerGameStats or get_PlayerGameQuarterStats or get_PlayerGameHalfStats
            ):
                def minutes_to_seconds(game_minutes):
                    if not game_minutes in [None, "DNP"] and not str(game_minutes) == "nan":
                        return int(game_minutes.split(":")[0]) * 60 + int(game_minutes.split(":")[1])
                    else:
                        return None
                
                games["seconds_played"] = games["minutes_played"].apply(lambda x: minutes_to_seconds(x))
                del games["minutes_played"]
        except Exception as e:
            handle_err(e, games=games)
        return games

    ###########################################################
    target_table_count = 0
    if get_TeamGameStats:
        TABLE_NAME = "TeamGameStats"
        target_table_count += 1
    if get_TeamGameQuarterStats:
        TABLE_NAME = "TeamGameQuarterStats"
        target_table_count += 1
    if get_TeamGameHalfStats:
        TABLE_NAME = "TeamGameHalfStats"
        target_table_count += 1
    if get_PlayerGameStats:
        TABLE_NAME = "PlayerGameStats"
        target_table_count += 1
    if get_PlayerGameQuarterStats:
        TABLE_NAME = "PlayerGameQuarterStats"
        target_table_count += 1
    if get_PlayerGameHalfStats:
        TABLE_NAME = "PlayerGameHalfStats"
        target_table_count += 1

    # Backup table in use
    if debug:
        TABLE_NAME += "2"

    if target_table_count > 1:
        print("Only one table can be loaded at a time")
        exit(1)

    games = None
    try:

        begin_year = int(begin_year)
        stop_year = int(stop_year)
        year = begin_year
        games_paginated = None
        while year >= stop_year:
            with create_engine(conn_str).begin() as connection:
                connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

                with open(f"{TABLE_NAME}/json/{year}{TABLE_NAME}.jsonl", "r") as f:
                    games = pd.read_json(f, lines=True)

                games = clean_data(games)
                page = 1
                chunksize = 1000
                while page * chunksize < len(games):
                    try:
                        games_paginated = games.iloc[
                            (page - 1) * chunksize : page * chunksize
                        ]
                        games_paginated.to_sql(
                            name=TABLE_NAME,
                            con=connection,
                            if_exists="append",
                            chunksize=chunksize,
                            index=False,
                        )
                        with open("log.txt", "w") as f:
                            f.write(str(page))
                        page += 1
                    except Exception as e:
                        with open("log.txt", "a+") as f:
                            f.write(str(e))
                        break

                games_paginated=games.iloc[(page - 1) * chunksize :]
                games_paginated.to_sql(
                    name=TABLE_NAME,
                    con=connection,
                    if_exists="append",
                    chunksize=chunksize,
                    index=False,
                )
                year -= 1

                connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    except Exception as e:
        handle_err(e, games=games_paginated)
        breakpoint()


def rmdb(
    oldest_year: int,
    newest_year: int,
    get_TeamGameStats=False,
    get_TeamGameQuarterStats=False,
    get_TeamGameHalfStats=False,
    get_PlayerGameStats=False,
    get_PlayerGameQuarterStats=False,
    get_PlayerGameHalfStats=False,
):

    target_table_count = 0
    if get_TeamGameStats:
        TABLE_NAME = "TeamGameStats"
        target_table_count += 1
    if get_TeamGameQuarterStats:
        TABLE_NAME = "TeamGameQuarterStats"
        target_table_count += 1
    if get_TeamGameHalfStats:
        TABLE_NAME = "TeamGameHalfStats"
        target_table_count += 1
    if get_PlayerGameStats:
        TABLE_NAME = "PlayerGameStats"
        target_table_count += 1
    if get_PlayerGameQuarterStats:
        TABLE_NAME = "PlayerGameQuarterStats"
        target_table_count += 1
    if get_PlayerGameHalfStats:
        TABLE_NAME = "PlayerGameHalfStats"
        target_table_count += 1

    if target_table_count > 1:
        print("Only one table can be loaded at a time")
        exit(1)

    with engine.begin() as connection:
        # Games for each year start no earlier than september, so all games
        # between {oldest_year}0901 (Sept. 1) and {newest_year + 1}0901 are
        # deleted
        SQL = f"""
            DELETE FROM {TABLE_NAME}
            WHERE game_br_id > '{oldest_year}0901'
            AND game_br_id <= '{newest_year + 1}0901'
            """
        print(SQL)
        result = connection.execute(text(SQL))
        print(f"Rows deleted: {result.rowcount}")



if __name__ == "__main__":
    TeamGameStats.helper.setJSON(
        games,
        away_team_basic,
        home_team_basic,
        four_factors,
        inactive_players,
        away_team_advanced,
        home_team_advanced,
        home_tgs,
        away_tgs,
        file,
        year,
    )

    # getTeamGameStatsHTML
    # setTeamGameStatsJSON
    # setPlayerGameStatsJSON
    # lsJSON
    # rmJSON
    # lsdb
    # loadJSONToDB
    # clean_data
    # shift_decimal
    # rmdb
