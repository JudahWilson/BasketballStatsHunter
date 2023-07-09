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
        
#################################################
# Initialize Database
#################################################
# Create a database file
if not os.path.exists('basketball_stats.db'):
    #TODO refine initialization
    # Create a database connection
    conn = sqlite3.connect('basketball_stats.db')
    c = conn.cursor()

    # players
    c.execute('drop table if exists players;')
    c.execute('''
            create table players (
            id         integer primary key autoincrement,
            first_name varchar(35) null,
            last_name  varchar(35) null,
            height_cm  integer     null,
            weight_lb  integer     null,
            city       varchar(30) null,
            territory  varchar(30) null,
            country    varchar(30) null,
            birthdate  date        null,
            nba_debute date        null
        );

    '''
    )

    # player states
    c.execute('drop table if exists player_states;')
    c.execute('''
        create table player_states (
            id          integer primary key autoincrement,
            player_id   integer     null,
            team_states_id integer   null,
            team_id     integer     null,
            jersey_no   integer     null,
            position    varchar(3)  null,
            start_date  date        null,
            end_date    date        null,
            FOREIGN KEY(player_id) REFERENCES players(id),
            FOREIGN KEY(team_states_id) REFERENCES team_states(id),
            FOREIGN KEY(team_id) REFERENCES teams(id)
        );
    ''')

    # coaches
    c.execute('drop table if exists coaches;')
    c.execute('''
            create table coaches (
            id         integer primary key autoincrement,
            first_name varchar(35) null,
            last_name  varchar(35) null,
            birthdate  date        null,
            nba_debute date        null
        );

    '''
    )

    # player states
    c.execute('drop table if exists player_states;')
    c.execute('''
        create table player_states (
            id          integer primary key autoincrement,
            player_id   integer     null,
            team_states_id integer   null,
            team_id     integer     null,
            jersey_no   integer     null,
            position    varchar(3)  null,
            start_date  date        null,
            end_date    date        null,
            FOREIGN KEY(player_id) REFERENCES players(id),
            FOREIGN KEY(team_states_id) REFERENCES team_states(id),
            FOREIGN KEY(team_id) REFERENCES teams(id)
        );
    ''')

    # teams
    c.execute('drop table if exists teams;')
    c.execute(
        '''create table teams (
            id   integer primary key autoincrement,
            name varchar(50) null
        );
        '''
    )

    # team states
    c.execute('drop table if exists team_states;')
    c.execute('''
        create table team_states (
            id          integer primary key autoincrement,
            team_id     integer     null,
            city        varchar(30) null,
            territory   varchar(30) null,
            zip         varchar(10) null,
            country     varchar(30) null,
            start_date  date        null,
            end_date    date        null,
            FOREIGN KEY(team_id) REFERENCES teams(id)
        );
    ''')
    
    # seasons
    c.execute('drop table if exists seasons;')
    c.execute(
        '''create table seasons (
            id          integer primary key autoincrement,
            year_start  integer,
            year_end    integer,
            mvp         integer,
            champion    integer,
            FOREIGN KEY(mvp) REFERENCES players(id),
            FOREIGN KEY(champion) REFERENCES teams(id)
        );
        '''
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

#####################################################
# DB interface class
#####################################################
class DB:
    """
    An interface to the db
    """
    def __init__(self):
        self.conn = sqlite3.connect('basketball_stats.db')
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
    time.sleep(4)
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
            return jsonify({'status_code': 500, 'message': error_message, 'traceback': traceback_str})