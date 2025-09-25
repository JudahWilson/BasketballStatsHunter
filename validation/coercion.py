"""Functions that transform a value from one type into another"""

import re

from pydantic import TypeAdapter
from validation.schemas import SeasonsRange, SeasonsRangeInput


def seasons_range_input_to_seasons_range(
    seasons_range: SeasonsRangeInput,
) -> SeasonsRange:
    # TODO not doing validation at the moment
    TypeAdapter(SeasonsRangeInput).validate_python(seasons_range)

    oldest_year = None
    newest_year = None
    if "-" in seasons_range:
        if re.match(r"^\d{4}-\d{4}$", seasons_range):
            year1, year2 = seasons_range.split("-")
            if year1 < year2:
                oldest_year = int(year1)
                newest_year = int(year2)
            else:
                oldest_year = int(year2)
                newest_year = int(year1)
        else:
            raise ValueError("")
    else:
        newest_year = int(seasons_range)
        oldest_year = newest_year

    return SeasonsRange(season_start=newest_year, season_end=oldest_year)
