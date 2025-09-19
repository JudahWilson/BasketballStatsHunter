"""One-off script to populate the season_br_id to games table

Is this logic implemented in the code?"""

import sys

sys.path.append("..")
import os

print(os.getcwd())
from PerGameStats.core.utilities import *
from sqlalchemy import text
import re

with create_engine(conn_str).begin() as connection:
    # Get each season
    seasons = connection.execute(text("SELECT br_id FROM seasons")).fetchall()
    # For each seasoon

    for season in seasons:
        # get season_br_id
        # Set all games of that season with this season_br_id
        season_br_id = season[0]

        # The first year is the year before the year shown in the season br_id
        year_start = int(re.match(r".*(\d{4})", season[0]).group(1)) - 1

        # TODO fix to determine which league this is for
        query = f"""
            UPDATE games SET season_br_id = '{season_br_id}' 
            WHERE br_id > '{year_start}0901%'
                AND br_id < '{year_start + 1}0901%'
        """
        print(query)
        connection.execute(text(query))
