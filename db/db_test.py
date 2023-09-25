import os
from dotenv import load_dotenv

load_dotenv()    

import mysql.connector 
import pandas as pd

db = mysql.connector.connect(
    host=os.environ['PS_HOST'],
    user=os.environ['PS_USERNAME'],
    passwd=os.environ['PS_PASSWORD'],
    database=os.environ['PS_DATABASE'],
)
#-----------------------------------------
# create a cursor to execute queries
cursor = db.cursor()

# # execute the query
# cursor.execute(query)

# # commit the changes to the database
# db.commit()

# now select and print all rows
cursor.execute('select count(*) from Teams')
rows = cursor.fetchall()
for row in rows:
    print(row)

# close the connection
db.close()
#-----------------------------------------

# # x=pd.read_sql('select * from Teams', db)

# # with open('dump copy 2.sql', 'r',encoding='utf-8') as f:
# #     sql = f.readlines()
# # log=open('log','w',encoding='utf-8')
# # for line in sql:
        
# #     try:
# #         if not line.startswith('INSERT INTO Teams'):
# #             continue
        
# #         db.cursor().execute(line)
# #         db.commit()
# #         log.write(line)
# #     except:
# #         # show traceback, and error message to stdout
# #         import traceback
# #         traceback.print_exc()
# #         print(line) 
# #         print("ERROR")
# #         breakpoint()
        
# # db.close()
# # log.close()
#-----------------------------------------