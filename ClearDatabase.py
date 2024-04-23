import sqlite3

conn = sqlite3.connect('vodomjeri.db')

conn.execute('DELETE FROM Uplata')

conn.commit()
conn.close()