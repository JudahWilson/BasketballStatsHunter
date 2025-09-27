"""The main entry point where each command as defined"""

from typing import Optional
import typer
from validation.coercion import seasons_range_input_to_seasons_range
from validation.schemas import (
    InputDataFormatTarget,
    InputPerGameStatTable,
)

app = typer.Typer()


@app.command("pgs")
def pergamestats(
    format: InputDataFormatTarget = typer.Argument(
        None,
        case_sensitive=False,
    ),
    seasons_range: Optional[str] = typer.Option(
        None,
        "--seasons-range",
        "-s",
        help="Oldest season's start year to the most recent season's start year, hyphen separated [YYYY-YYYY] or just the most recent start year [YYYY]",
        callback=lambda x: seasons_range_input_to_seasons_range(x) if x else None,
    ),
    tables: Optional[InputPerGameStatTable] = typer.Option(
        None,
        "--tables",
        "-t",
        show_default=False,
    ),
    file: bool = typer.Option(
        False,
        "--file",
        "-f",
        help="Gather all program controls from controls.json instead of CLI args",
    ),
):
    """Process per-game stats."""
    # TODO Your logic here
    typer.echo(
        f"format={format}, seasons_range={seasons_range}, tables={tables}, file={file}"
    )


# TODO play by play command


if __name__ == "__main__":
    app()
