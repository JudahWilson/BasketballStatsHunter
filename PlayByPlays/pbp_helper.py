import pandas as pd
import json
from json import JSONEncoder
import bs4
import os, re
import time
import traceback
import pyperclip
import requests
import jsonlines
import glob
from dotenv import load_dotenv
from sqlalchemy import create_engine
import numpy as np
from enum import Enum
from pydantic import BaseModel

WEBSCRAPE_DEBOUNCER = 4 # seconds to wait between web requests

load_dotenv()
conn_str = f"mysql+mysqlconnector://{os.environ['BACKEND_DB_USER']}:{os.environ['BACKEND_DB_PASSWORD']}@{os.environ['BACKEND_DB_HOST']}/{os.environ['BACKEND_DB_NAME']}"
engine = create_engine(conn_str)

# The website's base url
base_url = 'https://www.basketball-reference.com'

    
class PlayNotYetSupportedError(Exception):
    pass

class ActionMap(Enum):
    assist='assist'

class PlayAction(BaseModel):
    action: ActionMap
    player_br_id: str | None = None
    team_br_id: str | None = None
    
class Play(BaseModel):
    game_br_id: str
    plays: list[PlayAction]
    quarter: int
    clock_time: str
    home_score: int
    away_score: int
    distance_feet: int | None = None


def handle_err(e, game=None,additional_message=None):
    print('----------------')
    print('ERROR: ' + str(e) + '\n')
    traceback.print_exc()
    if game is not None:
        print('\nGame details:')
        print(game)
    if additional_message:
        print(additional_message)
    
    breakpoint()
    print('----------------')


class CustomEncoder(JSONEncoder):
     def default(self, obj):
         if isinstance(obj, np.int64):
             return int(obj)
         return super().default(obj)

def get_pbp_filename(game_br_id):
    year = game_br_id[:4]
    return f'html/{year}/PlayByPlay-{game_br_id}.html'


def get_player_br_id_from_url(href):
    """extract the player_br_id from a given player url

    Args:
        url (str): A link to a player description page
    """
    return href.split("/")[-1].replace(".html", "")


def get_soup(url):
    """
    Get a BeautifulSoup object from a url

    Args:
        url (str): the url to get the soup from

    Raises:
        Exception: A failure to get the data from the url

    Returns:
        BeautifulSoup: the soup object
    """
    print(url)
    response = requests.get(url)
    time.sleep(WEBSCRAPE_DEBOUNCER)
    if response.status_code < 200 or response.status_code > 299:
        time.sleep(10)
        print('RETRY')
        response = requests.get(url)
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f'Error getting data from {url}. Status ' + str(response.status_code))

    return bs4.BeautifulSoup(response.text, 'html.parser')