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

WEBSCRAPE_DEBOUNCER = 4 # seconds to wait between web requests

load_dotenv()
conn_str = f"mysql+mysqlconnector://{os.environ['BACKEND_DB_USER']}:{os.environ['BACKEND_DB_PASSWORD']}@{os.environ['BACKEND_DB_HOST']}/{os.environ['BACKEND_DB_NAME']}"
engine = create_engine(conn_str)

# The website's base url
base_url = 'https://www.basketball-reference.com'


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



def save_html(game, year):
    print(game['br_id'])

    try:
        url = base_url + "/boxscores/pbp/" + game['br_id'] + ".html"
    except Exception as e:
        breakpoint()
        breakpoint()
    soup = get_soup(url)
    
    # TODO get all plays all quarters
    try:
        html = str(soup.select('#pbp')[0])
        
        # TODO write 1 html file per game in 'html' folder 
        
        # If the year folder isn't there, create it
        if not os.path.exists(f'html/{year}'):
            os.makedirs(f'html/{year}')
        
        with open(f'html/{year}/PlayByPlay-{game["br_id"]}.html', 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        breakpoint()
        breakpoint()