from core.core import (
    writeTeamGameStatsHTML,
    writeTeamGameStatsJSON,
    writePlayerGameStatsJSON,
    lsJSON,
    rmJSON,
    lsdb,
    loadJSONToDB,
    rmdb,
)


# setTeamGameStatsJSON(
#     2023,
#     2022,
#     get_TeamGameStats=False,
#     get_TeamGameQuarterStats=False,
#     get_TeamGameHalfStats=False,
#     get_TeamGameOvertimeStats=True,
# )


writeTeamGameStatsHTML(
    start_year=2023,
    stop_year=2023,
    singular_game_br_id=None,
    override_existing_html=False,
)
