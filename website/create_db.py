#used to create db and table
import sqlite3 as sql

#connect to SQLite
con = sql.connect('db_plants.db')

#Create a Connection
cur = con.cursor()

#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS plants")

#Create users table  in db_web database
sql ='''CREATE TABLE "Plants" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Sort"	TEXT,
    "Planted"	DATE,
    "Harvested"	DATE,
    "Location"	TEXT,
	"Description"	TEXT
)'''
cur.execute(sql)

#commit changes
con.commit()

#close the connection
con.close()

# Path: website/app.py
# Compare this snippet from website/app.py:
# # Description: This is the main file of the website