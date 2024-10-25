import sqlite3
import json

dbfile = 'data\database.db'

conn = sqlite3.connect(dbfile, check_same_thread=False)

cursor = conn.cursor()

cursor.execute("SELECT * FROM Questions")

print(cursor.fetchall())