import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, email text, organization text, address text, password text)"
cursor.execute(create_table)

connection.commit()

connection.close()