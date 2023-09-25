import os
import mysql.connector 
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# establish a connection to the database
ps_db = mysql.connector.connect(
    host='aws.connect.psdb.cloud',
    user='gldu8hlddg4nt34zocdr',
    passwd='pscale_pw_3qk5CQZlCIIroDBI5F2AO1j8CiWbSx9phzPNx98GaU9',
    database='data',
)

print(pd.read_sql('select * from mysql.user', ps_db))
# # do the above but without a dataframe
# cursor = db.cursor()
# cursor.execute('select * from players')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
    
    

# # create a cursor to execute queries
# cursor = db.cursor()

# # create an insert statement
# query = """
#     INSERT INTO players (first_name, last_name, city, territory, country, birthdate, br_id, full_name, suffix, year_start, year_end, position, height_str, height_in, weight, birth_date, colleges)
#     VALUES ('Michael', 'Jordan', 'Brooklyn', 'New York', 'USA', '1963-02-17', 'jordami01', 'Michael Jordan', '', '1985', '2003', 'G', '6-6', 78, 195, '1963-02-17', '["UNC"]')
# """

# # execute the query
# cursor.execute(query)

# # commit the changes to the database
# db.commit()

# # now select and print all rows
# cursor.execute('SELECT * FROM players')
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# # close the connection
# db.close()

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