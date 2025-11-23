"""Functions that transform a value from one type into another"""

import re
from typing import cast

from pydantic import TypeAdapter
from validation.schemas import PerGameStatTableName, SeasonsRange, SeasonsRangeInput


def seasons_range_input_to_object(
    seasons_range: SeasonsRangeInput,
) -> SeasonsRange:
    # TODO not doing validation at the moment
    TypeAdapter(SeasonsRangeInput).validate_python(seasons_range)

    oldest_year = None
    newest_year = None
    if "-" in seasons_range:
        year1, year2 = seasons_range.split("-")
        if year1 < year2:
            oldest_year = int(year1)
            newest_year = int(year2)
        else:
            oldest_year = int(year2)
            newest_year = int(year1)
    else:
        newest_year = int(seasons_range)
        oldest_year = newest_year

    return SeasonsRange(newest_year_start=newest_year, season_end=oldest_year)


def tables_input_to_list(tables_csv: str | None) -> list[PerGameStatTableName]:
    """Convert tables name input CSV to a list and unabbreviate the abbreviations

    Args:
        tables_csv (str): A single line of comma separated table names or abbreviations

    Returns:
        list[PerGameStatTableName]: A list of unabbreviated table names
    """
    if not tables_csv:
        return []
    pgs_table_name_type = TypeAdapter(PerGameStatTableName)
    tables = tables_csv.split(",")
    unabbreviated_tables = []
    for t in tables:
        unabbreviated_name = unabbreviate_table_name(cast(PerGameStatTableName, t))
        pgs_table_name_type.validate_python(unabbreviated_name)
        unabbreviated_tables.append(unabbreviated_name)

    return cast(list[PerGameStatTableName], tables)


def unabbreviate_table_name(table_abbr: PerGameStatTableName):
    """Convert abbreviated table name to the actual table name

    Args:
        table_abbr (PerGameStatTableName): Name of table being unabbreviated
    """
    match table_abbr:
        case "tgs":
            return "teamgamestats"
        case "tgqs":
            return "teamgamequarterstats"
        case "tghs":
            return "teamgamehalfstats"
        case "tgos":
            return "teamgameovertimestats"
        case "pgs":
            return "playergamestats"
        case "pgqs":
            return "playergamequarterstats"
        case "pghs":
            return "playergamehalfstats"
        case "pgos":
            return "playergameovertimestats"
