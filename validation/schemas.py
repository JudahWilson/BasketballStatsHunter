"""Custom types definitions"""

from datetime import date
from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel
from enum import Enum


########################################
# region custom primitive types
########################################
PerGameStatTableName = Literal[
    "teamgamestats",
    "teamgamequarterstats",
    "teamgamehalfstats",
    "teamgameovertimestats",
    "playergamestats",
    "playergamequarterstats",
    "playergamehalfstats",
    "playergameovertimestats",
]
"""table names for per-game stats scripts."""

PerGameTeamStatTableName = Literal[
    "teamgamestats",
    "teamgamequarterstats",
    "teamgamehalfstats",
    "teamgameovertimestats",
]
"""table names for per-game stats scripts."""


PerGamePlayerStatTableName = Literal[
    "playergamestats",
    "playergamequarterstats",
    "playergamehalfstats",
    "playergameovertimestats",
]
"""table names for per-game stats scripts."""


class InputDataFormatTarget(str, Enum):
    """CLI arg for action being performed on data"""

    json = "json"
    db = "db"
    html = "html"
    rmjson = "rmjson"
    lsjson = "lsjson"
    lsdb = "lsdb"
    rmdb = "rmdb"


### GameBrId
def validate_game_br_id(value: str):
    year = value[0:4]
    month = value[5:7]
    day = value[7:9]

    # first 4 characters are a digit between 1946 and 2100
    if not (year.isdigit() and 1946 <= int(year) <= 2100):
        raise ValueError(
            "First four digits of the GameBrId must be between 1946 and 2100"
        )

    # 5th character is a 0
    if value[4] != "0":
        raise ValueError("5th character of the GameBrId must be a 0")
    # 6th and 7th characters are a digit between 1 and 12
    if not (month.isdigit() and 1 <= int(month) <= 12):
        raise ValueError(
            "6th and 7th characters of the GameBrId must be between 01 and 12"
        )

    # 8th and 9th characters are a valid day of the month using the month
    try:
        date(int(year), int(month), int(day))
    except ValueError:
        raise ValueError(
            f"The date (8th and 9th characters) in the GameBrId is an invalid date: {year}-{month}-{day}"
        )

    return value


GameBrId = Annotated[str, validate_game_br_id]
"""A Basketball Reference Game ID (GameBrId) string in the format YYYY0MMDDXXX
    - YYYY = 4-digit year
    - MM = 2-digit month
    - DD = 2-digit day, 
    - XXX = TeamBrId of the home team (3 characters)
"""


### SeasonsRangeInput
def validate_seasons_range_input(value: str):
    """Validate a seasons range input string.
    The input can be a single year (YYYY) or a range of years (YYYY-YYYY).
    Args:
        value (str): The input string to validate.
    Raises:
        ValueError: If the input is not in the correct format or out of range.
    Returns:
        str: The validated input string.
    """
    if "-" in value:
        start_year, end_year = value.split("-")
        print(f"{start_year=}")
        print(f"{end_year=}")
        if not (start_year.isdigit() and end_year.isdigit()):
            raise ValueError(
                "Both start year and end year must be digits in the format YYYY-YYYY"
            )
        if not (1946 <= int(start_year) <= 2100):
            raise ValueError("Start year must be between 1946 and 2100")
        if not (1946 <= int(end_year) <= 2100):
            raise ValueError("End year must be between 1946 and 2100")
        if int(start_year) > int(end_year):
            raise ValueError("Start year cannot be greater than end year")
    else:
        if not value.isdigit():
            raise ValueError("Year must be a digit in the format YYYY")
        if not (1946 <= int(value) <= 2100):
            raise ValueError("Year must be between 1946 and 2100")

    return value


SeasonsRangeInput = Annotated[str, AfterValidator(validate_seasons_range_input)]

########################################
# endregion custom primitive types
########################################


########################################
# region Pydantic models
########################################
class SeasonsRange(BaseModel):
    season_start: int
    """Start year of the season (YYYY)."""
    season_end: int
    """End year of the season (YYYY)."""


########################################
# endregion Pydantic models
########################################
