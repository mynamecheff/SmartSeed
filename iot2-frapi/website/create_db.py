#used to create db and table
import sqlite3 as sql

#connect to SQLite
con = sql.connect('db_plants.db')

#Create a Connection
cur = con.cursor()

#Create users table  in db_web database
sql ='''CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value1 FLOAT,
    value2 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)'''
cur.execute(sql)

#commit changes
con.commit()

#close the connection
con.close()

# Path: website/app.py
# Compare this snippet from website/app.py:
# # Description: This is the main file of the website