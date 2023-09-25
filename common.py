"""
This Module's purpose is to make project-wide functions and variables available,
as well as initialize the database if it doesn't exist. Basically, it will make
you equiped to work on this project.

The logger, database interface, and base url are all defined here so that they
can be used in multiple places.
"""

import sqlite3
import os
import traceback
from datetime import datetime
import requests
import time
import bs4
from flask import jsonify

WEBSCRAPE_DEBOUNCER = 4 # seconds to wait between web requests

# The website's base url
base_url = 'https://www.basketball-reference.com'

#################################################
# Initialize the logger
#################################################
class Log:
    """
    Official logger for the project. Logs are stored in the format of TIMESTAMP
    | MESSAGE in the logs/log.txt file.
    """    
    def __init__(self, filename):
        pass

    @staticmethod
    @property
    def logpath():
        """
        The path to the log file.
        Returns:
            str: logs/log.txt
        """
        return 'logs/log.txt'
    
    @staticmethod
    def log(message):
        """
        log a message to the log file. The log format is TIMESTAMP | MESSAGE

        Args:
            message (str): The information to log
        """
        with open(Log.logpath, 'a+') as f:
            f.write(message + ' | ' + str(datetime.now()))
        
def log(message):
    """
    The easy-to-access function to log a message to the log file. The log format
    is TIMESTAMP | MESSAGE

    Args:
        message (str): The information to log
    """
    Log.log(message)
        
#####################################################
# DB interface class
#####################################################
class DB:
    """
    An interface to the db
    """
    def __init__(self):
        self.conn = sqlite3.connect('basketball_stats.db') # TODO
        # self.conn.execute('SELECT load_extension("json1")') # Enable the JSON1 extension
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def select(self, query):
        try:
            assert 'update' not in query.lower(), 'Use update() for update queries'
            assert 'insert' not in query.lower(), 'Use insert() for insert queries'
            assert 'delete' not in query.lower(), 'Use delete() for delete queries'

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None
        
    def update(self, query):
        try:
            assert 'select' not in query.lower(), 'Use select() for select queries'
            assert 'insert' not in query.lower(), 'Use insert() for insert queries'
            assert 'delete' not in query.lower(), 'Use delete() for delete queries'

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None
        
    def insert(self, query):
        
        try:
            assert 'select' not in query.lower(), 'Use select() for select queries'
            assert 'update' not in query.lower(), 'Use update() for update queries'
            assert 'delete' not in query.lower(), 'Use delete() for delete queries'

            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None

# The project's database variable
db = DB() 


#####################################################
# Helper functions
#####################################################
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
        raise Exception(f'Error getting data from {url}. Status ' + str(response.status_code))

    return bs4.BeautifulSoup(response.text, 'html.parser')

def error_response(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            traceback_str = traceback.format_exc()
            return {'status_code': 500, 'message': error_message, 'traceback': traceback_str}