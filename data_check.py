import sqlite3

db_file = 'data\database.db'

conn = sqlite3.connect(db_file, check_same_thread=False)

cursor = conn.cursor()

cursor.execute("SELECT * FROM Feedback")

print(cursor.fetchall())