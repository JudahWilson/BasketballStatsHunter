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
import mysql.connector 
from dotenv import load_dotenv

load_dotenv()

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
    from sqlalchemy import create_engine
    from fastapi import HTTPException
    
    # conn = mysql.connector.connect(
    #     host=os.environ['BACKEND_DB_HOST'],
    #     user=os.environ['BACKEND_DB_USER'],
    #     passwd=os.environ['BACKEND_DB_PASSWORD'],
    #     database=os.environ['BACKEND_DB_NAME'],
    # )
    # cursor = conn.cursor()
    
    conn_str = f"mysql+mysqlconnector://{os.environ['BACKEND_DB_USER']}:{os.environ['BACKEND_DB_PASSWORD']}@{os.environ['BACKEND_DB_HOST']}/{os.environ['BACKEND_DB_NAME']}"
    print(conn_str)
    _engine = create_engine(conn_str)

    @staticmethod
    def simple_check_sql_injection(sql: str):
        '''
        Checks for SQL injection in a sql statement. 
        '''
        if '--' in sql or '/*' in sql or '*/' in sql or 'delete ' in sql.lower() \
        or 'insert ' in sql.lower() or 'update ' in sql.lower() or 'union ' in sql.lower():
            raise DB.HTTPException(status_code=500, detail='SQL statement could not be executed: SQL injection detected')

    @staticmethod
    def select(sql: str):
        try:
            assert 'update' not in sql.lower(), 'Use update() for update queries'
            assert 'insert' not in sql.lower(), 'Use insert() for insert queries'
            assert 'delete' not in sql.lower(), 'Use delete() for delete queries'

            DB.cursor.execute(sql)
            data = DB.cursor.fetchall()
            columns = [col[0] for col in DB.cursor.description]
            data = [dict(zip(columns, row)) for row in data]
            return data
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None
    
    @staticmethod 
    def update(query):
        try:
            assert 'select' not in query.lower(), 'Use select() for select queries'
            assert 'insert' not in query.lower(), 'Use insert() for insert queries'
            assert 'delete' not in query.lower(), 'Use delete() for delete queries'

            DB.cursor.execute(query)
            DB.conn.commit()
            
            return DB.cursor.fetchall()
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None
    
    @staticmethod    
    def insert(query):
        
        try:
            assert 'select' not in query.lower(), 'Use select() for select queries'
            assert 'update' not in query.lower(), 'Use update() for update queries'
            assert 'delete' not in query.lower(), 'Use delete() for delete queries'

            DB.cursor.execute(query)
            DB.conn.commit()
            
            return DB.cursor.fetchall()
        except Exception as e:
            # display traceback including line #
            traceback.print_exc()
            print(str(e))
            return None
        
    @staticmethod
    def close():
        # DB.conn.close()
        pass


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
