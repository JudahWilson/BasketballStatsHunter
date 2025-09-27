"""The main entry point where each command as defined"""

from typing import Optional
import typer
import subprocess
import os
from validation.coercion import seasons_range_input_to_seasons_range
from validation.schemas import (
    InputDataFormatTarget,
    InputPerGameStatTable,
)
import HuntApp


app = typer.Typer()
app.add_typer(HuntApp.app, name="hunt")


@app.command()
def frontend():
    """Fire up metabase and ngrok for the frontend to be public."""
    os.chdir("metabase")
    subprocess.Popen(["java", "-jar", "metabase.jar"])
    subprocess.Popen(["ngrok", "http", "--domain=judahwilson.ngrok.io", "3000"])


if __name__ == "__main__":
    app()
