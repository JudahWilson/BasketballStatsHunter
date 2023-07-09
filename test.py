'''
establish a connection to a planetscale db given these env variables

HOST=aws.connect.psdb.cloud
USERNAME=pozwzl1mek3tudhk5auf
PASSWORD=pscale_pw_SX4XCY7UaQ0WloA8ZMqLQAy3nrguNAY4WBVEXtGP2r4
DATABASE=basketballstats
SSL_CERT=cacert-2023-05-30.pem
'''

import os
import mysql.connector 
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# establish a connection to the database
PlanetScale_conn = mysql.connector.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USERNAME'),
    passwd=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE'),
    ssl_ca=os.getenv('SSL_CERT')
)

print(pd.read_sql('select * from players', PlanetScale_conn))


from project import *

x = pd.read_sql('select * from players', db.conn)

# x.to_sql('players', PlanetScale_conn)

# how to import into table using pandas if using mysql without sqlalchemy
x.to_sql('players', PlanetScale_conn, if_exists='append', index=False)

################
# # create a cursor to execute queries
# cursor = db.cursor()

# # # create an insert statement
# # query = """
# #     INSERT INTO players (first_name, last_name, city, territory, country, birthdate, br_id, full_name, suffix, year_start, year_end, position, height_str, height_in, weight, birth_date, colleges)
# #     VALUES ('Michael', 'Jordan', 'Brooklyn', 'New York', 'USA', '1963-02-17', 'jordami01', 'Michael Jordan', '', '1985', '2003', 'G', '6-6', 78, 195, '1963-02-17', '["UNC"]')
# # """

# # # execute the query
# # cursor.execute(query)

# # # commit the changes to the database
# # db.commit()

# # now select and print all rows
# cursor.execute('SELECT * FROM players')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# close the connection
PlanetScale_conn.close()

'''
CREATE TABLE players (
  id INT(11) NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(35),
  last_name VARCHAR(35),
  city VARCHAR(30),
  territory VARCHAR(30),
  country VARCHAR(30),
  birthdate DATE,
  br_id CHAR(8),
  full_name VARCHAR(50),
  suffix VARCHAR(5),
  year_start CHAR(4),
  year_end CHAR(4),
  position VARCHAR(5),
  height_str CHAR(4),
  height_in INT(11),
  weight INT(11),
  birth_date DATE,
  colleges JSON,
  PRIMARY KEY (id)
);
'''