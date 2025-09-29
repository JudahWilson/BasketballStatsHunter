"""The main entry point where each command as defined"""

import typer
import subprocess
import os
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
