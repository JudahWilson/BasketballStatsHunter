"""The main entry point where each command as defined"""

from typing import Optional, cast
import typer
from validation.coercion import (
    seasons_range_input_to_object,
    tables_input_to_list,
)
from validation.schemas import (
    InputDataFormatTarget,
)

app = typer.Typer(
    no_args_is_help=True,
    help="This app process this workflow:"
    "\n1. Download data as html"
    "\n2. Convert html to jsonl"
    "\n3. Load jsonl data into the database"
    "\nSometimes step 1 and 2 is done in one swing.",
)
from HuntApp.PerGameStats.core import (
    writeTeamGameStatsHTML,
    writeTeamGameStatsJSON,
    writePlayerGameStatsJSON,
    lsJSON,
    rmJSON,
    lsdb,
    loadJSONToDB,
    rmdb,
)


@app.command("pgs")
def pergamestats(
    target: InputDataFormatTarget = typer.Argument(
        None,
        case_sensitive=False,
    ),
    seasons_range_inp: Optional[str] = typer.Option(
        None,
        "--seasons-range",
        "-s",
        help="Oldest season's start year to the most recent season's start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]",
    ),
    tables_inp: Optional[str] = typer.Option(
        None,
        "--tables",
        "-t",
        help="comma separated list of table names or their abbreviations",
    ),
):
    """Process per-game stats."""
    seasons_range = None
    tables = None

    if seasons_range_inp:
        seasons_range = seasons_range_input_to_object(seasons_range_inp)
    if tables_inp:
        tables = tables_input_to_list(tables_inp)

    # Additional input requirements
    if target in ["json", "db", "rmjson"] and not tables:
        raise Exception(f"--tables (-t) is required for {target}")
    if target not in ["lsjson", "lsdb"] and not seasons_range:
        raise Exception(f"--seasons-range (-s) is required for {target}")

    typer.echo("INPUT")
    typer.echo(
        f"target={target}, seasons_range={seasons_range_inp}, tables={tables_inp}"
    )
    typer.echo("INPUT CONVERTED")
    typer.echo(
        f"target={target}, seasons_range={seasons_range if seasons_range else None}, tables={tables if tables else None}"
    )


# TODO play by play command


if __name__ == "__main__":
    app()
