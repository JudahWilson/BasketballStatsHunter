# TODO
import pandas as pd
import pyperclip
from io import StringIO
import pyperclip


def setPlayersData(game, quarter, is_home, four_factors, team_stats_q) -> list:
    # Get DataFrane of basic stats
    DF_pls_basic = pd.read_html(StringIO(str(team_stats_q)))
    DF_pls_basic = DF_pls_basic[0]
    DF_pls_basic.columns = DF_pls_basic.columns.droplevel(0)
    # remove row that function as headers
    DF_pls_basic = DF_pls_basic[DF_pls_basic["Starters"] != "Reserves"]

    # Get soup object list over the same basic data
    SP_pl_basic = team_stats_q.find("tbody").find_all("tr")
    # remove row that function as headers
    SP_pl_basic = [
        element for element in SP_pl_basic if "thead" not in element.get("class", [])
    ]

    # convert to index based loop to deal with basic and advanced simultaneously
    index = 0
    pgs_list = []
    while index < len(SP_pl_basic):
        SP_player = SP_pl_basic[index]
        if "Reserves" in SP_player.text:
            continue  # This is a header row, not data

        DF_pl_basic = DF_pls_basic.iloc[index]

        pgs = {}

        pgs["player_br_id"] = SP_player.th.a["href"].split("/")[-1].replace(".html", "")
        pgs["game_br_id"] = game["br_id"]
        pgs["quarter"] = quarter

        # some don'tplay for a quarter
        if (
            str(DF_pl_basic.MP) == "nan"
            or "Did Not Play" in SP_player.text
            or "Did Not Dress" in SP_player.text
            or "Not With Team" in SP_player.text
            or "Player Suspended" in SP_player.text
        ):
            played = False
        else:
            played = True

        if is_home:
            pgs["team_br_id"] = four_factors.select('[data-stat="team_id"] > a')[0].text
        else:
            pgs["team_br_id"] = four_factors.select('[data-stat="team_id"] > a')[1].text

        if not played:
            pgs["minutes_played"] = None
            pgs["field_goals"] = None
            pgs["field_goal_attempts"] = None
            pgs["field_goal_percentage"] = None
            pgs["three_pointers"] = None
            pgs["three_pointer_attempts"] = None
            pgs["three_pointer_percentage"] = None
            pgs["free_throws"] = None
            pgs["free_throw_attempts"] = None
            pgs["free_throw_percentage"] = None
            pgs["rebounds"] = None
            pgs["offensive_rebounds"] = None
            pgs["defensive_rebounds"] = None
            pgs["assists"] = None
            pgs["steals"] = None
            pgs["blocks"] = None
            pgs["turnovers"] = None
            pgs["personal_fouls"] = None
            pgs["points"] = None
            pgs["plus_minus"] = None

        else:
            next_field = "minutes_played"
            pgs["minutes_played"] = DF_pl_basic["MP"]
            next_field = "field_goals"
            pgs["field_goals"] = DF_pl_basic["FG"]
            next_field = "field_goal_attempts"
            pgs["field_goal_attempts"] = DF_pl_basic["FGA"]
            next_field = "field_goal_percentage"
            pgs["field_goal_percentage"] = DF_pl_basic["FG%"]
            if "3P" in DF_pl_basic:
                pgs["three_pointers"] = DF_pl_basic["3P"]
            else:
                pgs["three_pointers"] = None
            next_field = "three_pointer_attempts"
            if "3PA" in DF_pl_basic:
                pgs["three_pointer_attempts"] = DF_pl_basic["3PA"]
            else:
                pgs["three_pointer_attempts"] = None
            next_field = "three_pointer_percentage"
            if "3P%" in DF_pl_basic:
                pgs["three_pointer_percentage"] = DF_pl_basic["3P%"]
            else:
                pgs["three_pointer_percentage"] = None
            next_field = "free_throws"
            pgs["free_throws"] = DF_pl_basic["FT"]
            next_field = "free_throw_attempts"
            pgs["free_throw_attempts"] = DF_pl_basic["FTA"]
            next_field = "free_throw_percentage"
            pgs["free_throw_percentage"] = DF_pl_basic["FT%"]
            next_field = "rebounds"
            pgs["rebounds"] = DF_pl_basic["TRB"]
            next_field = "offensive_rebounds"
            pgs["offensive_rebounds"] = DF_pl_basic["ORB"]
            next_field = "defensive_rebounds"
            pgs["defensive_rebounds"] = DF_pl_basic["DRB"]
            next_field = "assists"
            pgs["assists"] = DF_pl_basic["AST"]
            next_field = "steals"
            pgs["steals"] = DF_pl_basic["STL"]
            next_field = "blocks"
            pgs["blocks"] = DF_pl_basic["BLK"]
            next_field = "turnovers"
            pgs["turnovers"] = DF_pl_basic["TOV"]
            next_field = "personal_fouls"
            pgs["personal_fouls"] = DF_pl_basic["PF"]
            next_field = "points"
            pgs["points"] = DF_pl_basic["PTS"]
            try:
                pgs["plus_minus"] = int(DF_pl_basic["+/-"])
            except ValueError as e:
                pgs["plus_minus"] = None

        pgs_list.append(pgs)
        index += 1

    return pgs_list


def setPlayerGameQuarterStatsJson(
    game,
    quarter,
    away_team_q,
    home_team_q,
    four_factors,
):
    """
    Set the JSON object for the PlayerGameStats object.
    """
    print(game["url"])

    all_players = []

    # Home players
    all_players += setPlayersData(
        game,
        quarter,
        True,
        four_factors=four_factors,
        team_stats_q=home_team_q,
    )

    # Away players
    all_players += setPlayersData(
        game,
        quarter,
        False,
        four_factors=four_factors,
        team_stats_q=away_team_q,
    )

    return all_players
