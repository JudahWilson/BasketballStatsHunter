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


def run_command(controls: Controls):
    match controls.format:
        case "json":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameOvertimeStats = False

            if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats = True

            if "teamgamequarterstats" in controls.tables or "tgqs" in controls.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats = True

            if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats = True

            if "teamgameovertimestats" in controls.tables or "tgos" in controls.tables:
                print("Processing TeamGameOvertimeStats")
                get_TeamGameOvertimeStats = True

            if "playergamestats" in controls.tables or "pgs" in controls.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats = True

            if "playergamequarterstats" in controls.tables or "pgqs" in controls.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats = True

            if "playergamehalfstats" in controls.tables or "pghs" in controls.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats = True

            if (
                "playergameovertimestats" in controls.tables
                or "pgos" in controls.tables
            ):
                print("Processing PlayerGameOvertimeStats")
                get_PlayerGameOvertimeStats = True

            if (
                get_TeamGameStats
                or get_TeamGameQuarterStats
                or get_TeamGameHalfStats
                or get_TeamGameOvertimeStats
            ):
                writeTeamGameStatsJSON(
                    controls.newest_year,
                    controls.oldest_year,
                    get_TeamGameStats=get_TeamGameStats,
                    get_TeamGameHalfStats=get_TeamGameHalfStats,
                    get_TeamGameQuarterStats=get_TeamGameQuarterStats,
                    get_TeamGameOvertimeStats=get_TeamGameOvertimeStats,
                )
            if (
                get_PlayerGameStats
                or get_PlayerGameQuarterStats
                or get_PlayerGameHalfStats
                or get_PlayerGameOvertimeStats
            ):
                writePlayerGameStatsJSON(
                    controls.newest_year,
                    controls.oldest_year,
                    get_PlayerGameStats=get_PlayerGameStats,
                    get_PlayerGameHalfStats=get_PlayerGameHalfStats,
                    get_PlayerGameQuarterStats=get_PlayerGameQuarterStats,
                    get_PlayerGameOvertimeStats=get_PlayerGameOvertimeStats,
                )

        case "lsjson":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameOvertimeStats = False

            if controls.tables:
                if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                    get_TeamGameStats = True

                if (
                    "teamgamequarterstats" in controls.tables
                    or "tgqs" in controls.tables
                ):
                    get_TeamGameQuarterStats = True

                if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                    get_TeamGameHalfStats = True

                if (
                    "teamgameovertimestats" in controls.tables
                    or "tgos" in controls.tables
                ):
                    get_TeamGameOvertimeStats = True

                if "playergamestats" in controls.tables or "pgs" in controls.tables:
                    get_PlayerGameStats = True

                if (
                    "playergamequarterstats" in controls.tables
                    or "pgqs" in controls.tables
                ):
                    get_PlayerGameQuarterStats = True

                if (
                    "playergamehalfstats" in controls.tables
                    or "pghs" in controls.tables
                ):
                    get_PlayerGameHalfStats = True

                if (
                    "playergameovertimestats" in controls.tables
                    or "pgos" in controls.tables
                ):
                    get_PlayerGameOvertimeStats = True
            else:
                get_TeamGameStats = True
                get_TeamGameQuarterStats = True
                get_TeamGameHalfStats = True
                get_TeamGameOvertimeStats = True
                get_PlayerGameStats = True
                get_PlayerGameQuarterStats = True
                get_PlayerGameHalfStats = True
                get_PlayerGameOvertimeStats = True
            lsJSON(
                get_TeamGameStats,
                get_TeamGameQuarterStats,
                get_TeamGameHalfStats,
                get_TeamGameOvertimeStats,
                get_PlayerGameStats,
                get_PlayerGameQuarterStats,
                get_PlayerGameHalfStats,
                get_PlayerGameOvertimeStats,
            )

        case "rmjson":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameOvertimeStats = False

            if controls.tables:
                if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                    get_TeamGameStats = True

                if (
                    "teamgamequarterstats" in controls.tables
                    or "tgqs" in controls.tables
                ):
                    get_TeamGameQuarterStats = True

                if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                    get_TeamGameHalfStats = True

                if (
                    "teamgameovertimestats" in controls.tables
                    or "tgos" in controls.tables
                ):
                    get_TeamGameOvertimeStats = True

                if "playergamestats" in controls.tables or "pgs" in controls.tables:
                    get_PlayerGameStats = True

                if (
                    "playergamequarterstats" in controls.tables
                    or "pgqs" in controls.tables
                ):
                    get_PlayerGameQuarterStats = True

                if (
                    "playergamehalfstats" in controls.tables
                    or "pghs" in controls.tables
                ):
                    get_PlayerGameHalfStats = True

                if (
                    "playergameovertimestats" in controls.tables
                    or "pgos" in controls.tables
                ):
                    get_PlayerGameOvertimeStats = True
            else:
                get_TeamGameStats = True
                get_TeamGameQuarterStats = True
                get_TeamGameHalfStats = True
                get_TeamGameOvertimeStats = True
                get_PlayerGameStats = True
                get_PlayerGameQuarterStats = True
                get_PlayerGameHalfStats = True
                get_PlayerGameOvertimeStats = True

            rmJSON(
                controls.newest_year,
                controls.oldest_year,
                get_TeamGameStats,
                get_TeamGameQuarterStats,
                get_TeamGameHalfStats,
                get_TeamGameOvertimeStats,
                get_PlayerGameStats,
                get_PlayerGameQuarterStats,
                get_PlayerGameHalfStats,
                get_PlayerGameOvertimeStats,
            )

        case "lsdb":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameOvertimeStats = False

            if controls.tables:
                if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                    get_TeamGameStats = True

                if (
                    "teamgamequarterstats" in controls.tables
                    or "tgqs" in controls.tables
                ):
                    get_TeamGameQuarterStats = True

                if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                    get_TeamGameHalfStats = True

                if "playergamestats" in controls.tables or "pgs" in controls.tables:
                    get_PlayerGameStats = True

                if (
                    "playergamequarterstats" in controls.tables
                    or "pgqs" in controls.tables
                ):
                    get_PlayerGameQuarterStats = True

                if (
                    "playergamehalfstats" in controls.tables
                    or "pghs" in controls.tables
                ):
                    get_PlayerGameHalfStats = True
            else:
                get_TeamGameStats = True
                get_TeamGameQuarterStats = True
                get_TeamGameHalfStats = True
                get_TeamGameOvertimeStats = True
                get_PlayerGameStats = True
                get_PlayerGameQuarterStats = True
                get_PlayerGameHalfStats = True
                get_PlayerGameOvertimeStats = True
            lsdb(
                get_TeamGameStats,
                get_TeamGameQuarterStats,
                get_TeamGameHalfStats,
                get_TeamGameOvertimeStats,
                get_PlayerGameStats,
                get_PlayerGameQuarterStats,
                get_PlayerGameHalfStats,
                get_PlayerGameOvertimeStats,
            )

        case "db":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameOvertimeStats = False

            if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                print("Processing TeamGameStats")
                get_TeamGameStats = True

            if "teamgamequarterstats" in controls.tables or "tgqs" in controls.tables:
                print("Processing TeamGameQuarterStats")
                get_TeamGameQuarterStats = True

            if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                print("Processing TeamGameHalfStats")
                get_TeamGameHalfStats = True

            if "teamgameovertimestats" in controls.tables or "tgos" in controls.tables:
                print("Processing TeamGameOvertimeStats")
                get_TeamGameOvertimeStats = True

            if "playergamestats" in controls.tables or "pgs" in controls.tables:
                print("Processing PlayerGameStats")
                get_PlayerGameStats = True

            if "playergamequarterstats" in controls.tables or "pgqs" in controls.tables:
                print("Processing PlayerGameQuarterStats")
                get_PlayerGameQuarterStats = True

            if "playergamehalfstats" in controls.tables or "pghs" in controls.tables:
                print("Processing PlayerGameHalfStats")
                get_PlayerGameHalfStats = True

            if (
                "playergameovertimestats" in controls.tables
                or "pgos" in controls.tables
            ):
                print("Processing PlayerGameOvertimeStats")
                get_PlayerGameOvertimeStats = True

            loadJSONToDB(
                controls.newest_year,
                controls.oldest_year,
                get_TeamGameStats=get_TeamGameStats,
                get_TeamGameHalfStats=get_TeamGameHalfStats,
                get_TeamGameQuarterStats=get_TeamGameQuarterStats,
                get_TeamGameOvertimeStats=get_TeamGameOvertimeStats,
                get_PlayerGameStats=get_PlayerGameStats,
                get_PlayerGameHalfStats=get_PlayerGameHalfStats,
                get_PlayerGameQuarterStats=get_PlayerGameQuarterStats,
                get_PlayerGameOvertimeStats=get_PlayerGameOvertimeStats,
            )

        case "rmdb":
            get_TeamGameStats = False
            get_TeamGameHalfStats = False
            get_TeamGameQuarterStats = False
            get_TeamGameOvertimeStats = False
            get_PlayerGameStats = False
            get_PlayerGameQuarterStats = False
            get_PlayerGameHalfStats = False
            get_PlayerGameOvertimeStats = False

            if controls.tables:
                if "teamgamestats" in controls.tables or "tgs" in controls.tables:
                    get_TeamGameStats = True

                if (
                    "teamgamequarterstats" in controls.tables
                    or "tgqs" in controls.tables
                ):
                    get_TeamGameQuarterStats = True

                if "teamgamehalfstats" in controls.tables or "tghs" in controls.tables:
                    get_TeamGameHalfStats = True

                if (
                    "teamgameovertimestats" in controls.tables
                    or "tgos" in controls.tables
                ):
                    get_TeamGameOvertimeStats = True

                if "playergamestats" in controls.tables or "pgs" in controls.tables:
                    get_PlayerGameStats = True

                if (
                    "playergamequarterstats" in controls.tables
                    or "pgqs" in controls.tables
                ):
                    get_PlayerGameQuarterStats = True

                if (
                    "playergamehalfstats" in controls.tables
                    or "pghs" in controls.tables
                ):
                    get_PlayerGameHalfStats = True

                if (
                    "playergameovertimestats" in controls.tables
                    or "pgos" in controls.tables
                ):
                    get_PlayerGameOvertimeStats = True
            else:
                get_TeamGameStats = True
                get_TeamGameQuarterStats = True
                get_TeamGameHalfStats = True
                get_TeamGameOvertimeStats = True
                get_PlayerGameStats = True
                get_PlayerGameQuarterStats = True
                get_PlayerGameHalfStats = True
            rmdb(
                controls.oldest_year,
                controls.newest_year,
                get_TeamGameStats,
                get_TeamGameQuarterStats,
                get_TeamGameHalfStats,
                get_TeamGameOvertimeStats,
                get_PlayerGameStats,
                get_PlayerGameQuarterStats,
                get_PlayerGameHalfStats,
                get_PlayerGameOvertimeStats,
            )

        case "html":
            writeTeamGameStatsHTML(
                controls.newest_year, controls.oldest_year, override_existing_html=False
            )


def main():
    parser = build_parser()

    if len(sys.argv) == 1:
        # No args, get input using input() in a loop and rerun commands until user quits
        while True:
            print("\n-----------------------------------")
            input_command = input("Command (enter to exit): ")
            if input_command == "":
                break
            try:
                args = parser.parse_args(input_command.split())
            except Exception as e:
                print(f"Error: {e}")
                continue
            handle_input_command(args)
    else:
        args = parser.parse_args()
        handle_input_command(args)
