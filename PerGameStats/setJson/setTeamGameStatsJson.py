import pandas as pd
import pyperclip
from bs4 import BeautifulSoup, Tag


def setTeamGameStatsJson(
    games: pd.DataFrame,
    away_team_basic: Tag,
    home_team_basic: Tag,
    four_factors: Tag,
    inactive_players: Tag,
    away_team_advanced: Tag,
    home_team_advanced: Tag,
    home_tgs: dict,
    away_tgs: dict,
    file: str,
    year: int,
) -> None:
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
    game = games[games["br_id"] == file.split("-")[1].split(".")[0]].iloc[0]
    print(game["url"])

    home_tgs["game_id"] = game["id"]
    away_tgs["game_id"] = game["id"]

    home_tgs["game_br_id"] = game["br_id"]
    away_tgs["game_br_id"] = game["br_id"]

    away_tgs["team_br_id"] = away_team_basic.attrs["id"].split("-")[1]
    home_tgs["team_br_id"] = home_team_basic.attrs["id"].split("-")[1]

    away_tgs["minutes_played"] = (
        away_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
        if away_team_basic.select('td[data-stat="mp"]')[-1]
        else None
    )
    home_tgs["minutes_played"] = (
        home_team_basic.select('td[data-stat="mp"]')[-1].text.strip()
        if home_team_basic.select('td[data-stat="mp"]')[-1]
        else None
    )

    away_tgs["field_goals"] = (
        away_team_basic.select('[data-stat="fg"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="fg"]')[-1]
        else None
    )
    home_tgs["field_goals"] = (
        home_team_basic.select('[data-stat="fg"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="fg"]')[-1]
        else None
    )

    away_tgs["field_goal_attempts"] = (
        away_team_basic.select('[data-stat="fga"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="fga"]')[-1]
        else None
    )
    home_tgs["field_goal_attempts"] = (
        home_team_basic.select('[data-stat="fga"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="fga"]')[-1]
        else None
    )

    away_tgs["field_goal_percentage"] = (
        away_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="fg_pct"]')[-1]
        else None
    )
    home_tgs["field_goal_percentage"] = (
        home_team_basic.select('[data-stat="fg_pct"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="fg_pct"]')[-1]
        else None
    )

    if "three_pointers" in away_tgs:
        away_tgs["three_pointers"] = (
            away_team_basic.select('[data-stat="fg3"]')[-1].text.strip()
            if away_team_basic.select('[data-stat="fg3"]')[-1]
            else None
        )
        home_tgs["three_pointers"] = (
            home_team_basic.select('[data-stat="fg3"]')[-1].text.strip()
            if home_team_basic.select('[data-stat="fg3"]')[-1]
            else None
        )

        away_tgs["three_pointer_attempts"] = (
            away_team_basic.select('[data-stat="fg3a"]')[-1].text.strip()
            if away_team_basic.select('[data-stat="fg3a"]')[-1]
            else None
        )
        home_tgs["three_pointer_attempts"] = (
            home_team_basic.select('[data-stat="fg3a"]')[-1].text.strip()
            if home_team_basic.select('[data-stat="fg3a"]')[-1]
            else None
        )

        away_tgs["three_pointer_percentage"] = (
            away_team_basic.select('[data-stat="fg3_pct"]')[-1].text.strip()
            if away_team_basic.select('[data-stat="fg3_pct"]')[-1]
            else None
        )
        home_tgs["three_pointer_percentage"] = (
            home_team_basic.select('[data-stat="fg3_pct"]')[-1].text.strip()
            if home_team_basic.select('[data-stat="fg3_pct"]')[-1]
            else None
        )

    away_tgs["free_throws"] = (
        away_team_basic.select('[data-stat="ft"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="ft"]')[-1]
        else None
    )
    home_tgs["free_throws"] = (
        home_team_basic.select('[data-stat="ft"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="ft"]')[-1]
        else None
    )

    away_tgs["free_throw_attempts"] = (
        away_team_basic.select('[data-stat="fta"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="fta"]')[-1]
        else None
    )
    home_tgs["free_throw_attempts"] = (
        home_team_basic.select('[data-stat="fta"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="fta"]')[-1]
        else None
    )

    away_tgs["free_throw_percentage"] = (
        away_team_basic.select('[data-stat="ft_pct"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="ft_pct"]')[-1]
        else None
    )
    home_tgs["free_throw_percentage"] = (
        home_team_basic.select('[data-stat="ft_pct"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="ft_pct"]')[-1]
        else None
    )

    away_tgs["rebounds"] = (
        away_team_basic.select('[data-stat="trb"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="trb"]')[-1]
        else None
    )
    home_tgs["rebounds"] = (
        home_team_basic.select('[data-stat="trb"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="trb"]')[-1]
        else None
    )

    away_tgs["offensive_rebounds"] = (
        away_team_basic.select('[data-stat="orb"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="orb"]')[-1]
        else None
    )
    home_tgs["offensive_rebounds"] = (
        home_team_basic.select('[data-stat="orb"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="orb"]')[-1]
        else None
    )

    away_tgs["defensive_rebounds"] = (
        away_team_basic.select('[data-stat="drb"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="drb"]')[-1]
        else None
    )
    home_tgs["defensive_rebounds"] = (
        home_team_basic.select('[data-stat="drb"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="drb"]')[-1]
        else None
    )

    away_tgs["assists"] = (
        away_team_basic.select('[data-stat="ast"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="ast"]')[-1]
        else None
    )
    home_tgs["assists"] = (
        home_team_basic.select('[data-stat="ast"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="ast"]')[-1]
        else None
    )

    away_tgs["steals"] = (
        away_team_basic.select('[data-stat="stl"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="stl"]')[-1]
        else None
    )
    home_tgs["steals"] = (
        home_team_basic.select('[data-stat="stl"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="stl"]')[-1]
        else None
    )

    away_tgs["blocks"] = (
        away_team_basic.select('[data-stat="blk"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="blk"]')[-1]
        else None
    )
    home_tgs["blocks"] = (
        home_team_basic.select('[data-stat="blk"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="blk"]')[-1]
        else None
    )

    away_tgs["turnovers"] = (
        away_team_basic.select('[data-stat="tov"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="tov"]')[-1]
        else None
    )
    home_tgs["turnovers"] = (
        home_team_basic.select('[data-stat="tov"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="tov"]')[-1]
        else None
    )

    away_tgs["personal_fouls"] = (
        away_team_basic.select('[data-stat="pf"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="pf"]')[-1]
        else None
    )
    home_tgs["personal_fouls"] = (
        home_team_basic.select('[data-stat="pf"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="pf"]')[-1]
        else None
    )

    away_tgs["points"] = (
        away_team_basic.select('[data-stat="pts"]')[-1].text.strip()
        if away_team_basic.select('[data-stat="pts"]')[-1]
        else None
    )
    home_tgs["points"] = (
        home_team_basic.select('[data-stat="pts"]')[-1].text.strip()
        if home_team_basic.select('[data-stat="pts"]')[-1]
        else None
    )

    if four_factors:
        away_tgs["pace_factor"] = (
            four_factors.select('[data-stat="pace"]')[1].text.strip()
            if four_factors.select('[data-stat="pace"]')[1]
            else None
        )
        home_tgs["pace_factor"] = (
            four_factors.select('[data-stat="pace"]')[2].text.strip()
            if four_factors.select('[data-stat="pace"]')[2]
            else None
        )

        away_tgs["ft_per_fga"] = (
            four_factors.select('[data-stat="ft_rate"]')[1].text.strip()
            if four_factors.select('[data-stat="ft_rate"]')[1]
            else None
        )
        home_tgs["ft_per_fga"] = (
            four_factors.select('[data-stat="ft_rate"]')[2].text.strip()
            if four_factors.select('[data-stat="ft_rate"]')[2]
            else None
        )

        # No advanced stat tables
        if not away_team_advanced:
            away_tgs["offensive_rebound_percentage"] = (
                four_factors.select('[data-stat="ft_rate"]')[1].text.strip()
                if four_factors.select('[data-stat="ft_rate"]')[1]
                else None
            )
            home_tgs["offensive_rebound_percentage"] = (
                four_factors.select('[data-stat="ft_rate"]')[2].text.strip()
                if four_factors.select('[data-stat="ft_rate"]')[2]
                else None
            )

    # ------Advanced Stats------#
    if away_team_advanced:
        away_tgs["true_shooting_percentage"] = away_team_advanced.select(
            '[data-stat="ts_pct"]'
        )[-1].text.strip()
        home_tgs["true_shooting_percentage"] = home_team_advanced.select(
            '[data-stat="ts_pct"]'
        )[-1].text.strip()

        away_tgs["effective_field_goal_percentage"] = away_team_advanced.select(
            '[data-stat="efg_pct"]'
        )[-1].text.strip()
        home_tgs["effective_field_goal_percentage"] = home_team_advanced.select(
            '[data-stat="efg_pct"]'
        )[-1].text.strip()

        away_tgs["three_point_attempt_rate"] = away_team_advanced.select(
            '[data-stat="fg3a_per_fga_pct"]'
        )[-1].text.strip()
        home_tgs["three_point_attempt_rate"] = home_team_advanced.select(
            '[data-stat="fg3a_per_fga_pct"]'
        )[-1].text.strip()

        away_tgs["free_throw_attempt_rate"] = away_team_advanced.select(
            '[data-stat="fta_per_fga_pct"]'
        )[-1].text.strip()
        home_tgs["free_throw_attempt_rate"] = home_team_advanced.select(
            '[data-stat="fta_per_fga_pct"]'
        )[-1].text.strip()

        away_tgs["offensive_rebound_percentage"] = away_team_advanced.select(
            '[data-stat="orb_pct"]'
        )[-1].text.strip()
        home_tgs["offensive_rebound_percentage"] = home_team_advanced.select(
            '[data-stat="orb_pct"]'
        )[-1].text.strip()

        away_tgs["defensive_rebound_percentage"] = away_team_advanced.select(
            '[data-stat="drb_pct"]'
        )[-1].text.strip()
        home_tgs["defensive_rebound_percentage"] = home_team_advanced.select(
            '[data-stat="drb_pct"]'
        )[-1].text.strip()

        away_tgs["total_rebound_percentage"] = away_team_advanced.select(
            '[data-stat="trb_pct"]'
        )[-1].text.strip()
        home_tgs["total_rebound_percentage"] = home_team_advanced.select(
            '[data-stat="trb_pct"]'
        )[-1].text.strip()

        away_tgs["assist_percentage"] = away_team_advanced.select(
            '[data-stat="ast_pct"]'
        )[-1].text.strip()
        home_tgs["assist_percentage"] = home_team_advanced.select(
            '[data-stat="ast_pct"]'
        )[-1].text.strip()

        away_tgs["steal_percentage"] = away_team_advanced.select(
            '[data-stat="stl_pct"]'
        )[-1].text.strip()
        home_tgs["steal_percentage"] = home_team_advanced.select(
            '[data-stat="stl_pct"]'
        )[-1].text.strip()

        away_tgs["block_percentage"] = away_team_advanced.select(
            '[data-stat="blk_pct"]'
        )[-1].text.strip()
        home_tgs["block_percentage"] = home_team_advanced.select(
            '[data-stat="blk_pct"]'
        )[-1].text.strip()

        away_tgs["turnover_percentage"] = away_team_advanced.select(
            '[data-stat="tov_pct"]'
        )[-1].text.strip()
        home_tgs["turnover_percentage"] = home_team_advanced.select(
            '[data-stat="tov_pct"]'
        )[-1].text.strip()

        away_tgs["usage_percentage"] = away_team_advanced.select(
            '[data-stat="usg_pct"]'
        )[-1].text.strip()
        home_tgs["usage_percentage"] = home_team_advanced.select(
            '[data-stat="usg_pct"]'
        )[-1].text.strip()

        away_tgs["offensive_rating"] = away_team_advanced.select(
            '[data-stat="off_rtg"]'
        )[-1].text.strip()
        home_tgs["offensive_rating"] = home_team_advanced.select(
            '[data-stat="off_rtg"]'
        )[-1].text.strip()

        away_tgs["defensive_rating"] = away_team_advanced.select(
            '[data-stat="def_rtg"]'
        )[-1].text.strip()
        home_tgs["defensive_rating"] = home_team_advanced.select(
            '[data-stat="def_rtg"]'
        )[-1].text.strip()
    else:
        away_tgs["true_shooting_percentage"] = None
        home_tgs["true_shooting_percentage"] = None
        away_tgs["effective_field_goal_percentage"] = None
        home_tgs["effective_field_goal_percentage"] = None
        away_tgs["three_point_attempt_rate"] = None
        home_tgs["three_point_attempt_rate"] = None
        away_tgs["free_throw_attempt_rate"] = None
        home_tgs["free_throw_attempt_rate"] = None
        away_tgs["offensive_rebound_percentage"] = None
        home_tgs["offensive_rebound_percentage"] = None
        away_tgs["defensive_rebound_percentage"] = None
        home_tgs["defensive_rebound_percentage"] = None
        away_tgs["total_rebound_percentage"] = None
        home_tgs["total_rebound_percentage"] = None
        away_tgs["assist_percentage"] = None
        home_tgs["assist_percentage"] = None
        away_tgs["steal_percentage"] = None
        home_tgs["steal_percentage"] = None
        away_tgs["block_percentage"] = None
        home_tgs["block_percentage"] = None
        away_tgs["turnover_percentage"] = None
        home_tgs["turnover_percentage"] = None
        away_tgs["usage_percentage"] = None
        home_tgs["usage_percentage"] = None
        away_tgs["offensive_rating"] = None
        home_tgs["offensive_rating"] = None
        away_tgs["defensive_rating"] = None
        home_tgs["defensive_rating"] = None

    away_tgs["inactive_players"] = []
    home_tgs["inactive_players"] = []
    away_or_home = None
    if inactive_players:
        for tag in inactive_players.select("span, a"):
            if tag.name == "span":
                if away_or_home is None:
                    away_or_home = "away"
                elif away_or_home == "away":
                    away_or_home = "home"

            elif tag.name == "a":
                if away_or_home == "away":
                    away_tgs["inactive_players"].append(
                        tag["href"].split("/")[-1].replace(".html", "")
                    )
                elif away_or_home == "home":
                    home_tgs["inactive_players"].append(
                        tag["href"].split("/")[-1].replace(".html", "")
                    )
    else:
        away_tgs["inactive_players"] = []
        home_tgs["inactive_players"] = []
