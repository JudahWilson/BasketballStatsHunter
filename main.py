# https://github.com/fastapi/typer


from typing import Literal, Optional
from pydantic import TypeAdapter
import typer
import subprocess
import os
from validation.coercion import seasons_range_input_to_seasons_range
from validation.schemas import (
    InputDataFormatTarget,
    InputPerGameStatTable,
    SeasonsRange,
    SeasonsRangeInput,
)


app = typer.Typer()


@app.command()
def pgs(
    format: InputDataFormatTarget = typer.Argument(
        None,
        # help="?",
        case_sensitive=False,
    ),
    seasons_range: Optional[str] = typer.Argument(
        None,
        help="Oldest season's start year to the most recent season's start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]",
        callback=lambda x: seasons_range_input_to_seasons_range(x),
    ),
    tables: Optional[InputPerGameStatTable] = typer.Argument(
        None,
        show_default=False,
    ),
    file: bool = typer.Option(
        False,
        "--file",
        help="Gather all program controls from controls.json instead of CLI args",
    ),
):
    """Process per-game stats."""
    # TODO Your logic here
    typer.echo(
        f"format={format}, seasons_range={seasons_range}, tables={tables}, file={file}"
    )


@app.command()
def frontend():
    """Fire up metabase and ngrok for the frontend to be public."""
    os.chdir("metabase")
    subprocess.Popen(["java", "-jar", "metabase.jar"])
    subprocess.Popen(["ngrok", "http", "--domain=judahwilson.ngrok.io", "3000"])


if __name__ == "__main__":
    app()
