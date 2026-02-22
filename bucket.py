"""The main entry point where each command as defined"""

import typer
import subprocess
import os
import sys
import re
from dotenv import load_dotenv
import HuntApp

# Load environment variables from .env file
load_dotenv()


app = typer.Typer()
app.add_typer(HuntApp.app, name="hunt")


@app.command()
def frontend():
    """Fire up metabase and ngrok for the frontend to be public."""
    os.chdir("metabase")
    subprocess.Popen(["java", "-jar", "metabase.jar"])
    subprocess.Popen(["ngrok", "http", "--domain=judahwilson.ngrok.io", "3000"])


@app.command()
def export_ddl():
    """Export database DDL using mariadb-dump."""
    # Get database URL and extract components manually to avoid URL parsing issues
    db_url = os.getenv('PROD_DB_URL')
    
    # Parse URL manually: mysql+mysqlconnector://user:password@host/database?params
    # Pattern: scheme://user:password@host/database?query
    match = re.match(r'.*://([^:]+):([^@]+)@([^/]+)/([^?]+)', db_url)
    
    if not match:
        print("Error: Could not parse database URL")
        return
        
    username, password, hostname, database = match.groups()
    
    # Build the mariadb-dump command
    cmd = ["mariadb-dump", "-u", username, f"-p{password}", 
           "-h", hostname, "-d", database, "--no-data"]
    
    with open('ddl.sql', 'w') as f:
        subprocess.run(cmd, stdout=f)


if __name__ == "__main__":
    app()
