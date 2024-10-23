import sqlite3

dbfile = 'data\database.db'

conn = sqlite3.connect(dbfile, check_same_thread=False)

cursor = conn.cursor()
cursor.execute('SELECT * FROM Feedback')

for i in cursor.fetchall():
    print(i)