import sqlite3

conn = sqlite3.connect('vodomjeri.db')

conn.execute('DELETE FROM Ocitanje')

conn.commit()
conn.close()