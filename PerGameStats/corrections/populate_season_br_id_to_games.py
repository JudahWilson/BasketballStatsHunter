"""One-off script to populate the season_br_id to games table

Is this logic implemented in the code?"""
import sys
sys.path.append('..')
from core.helper import *
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
        year_start = int(re.match(r'.*(\d{4})', season[0]).group(1))
        print(f"""
            UPDATE games SET season_br_id = '{season_br_id}' 
            WHERE br_id > '{year_start}0901%'
                AND br_id < '{year_start + 1}0901%'
        """)
        connection.execute(text(f"""
            UPDATE games SET season_br_id = '{season_br_id}' 
            WHERE br_id > '{year_start}0901%'
                AND br_id < '{year_start + 1}0901%'
        """))

