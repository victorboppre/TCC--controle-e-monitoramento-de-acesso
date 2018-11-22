import sqlite3

conn = sqlite3.connect('login.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE login(login TEXT, password TEXT, nivel INTEGER);""")
print('TAbela criada')
conn.close()

