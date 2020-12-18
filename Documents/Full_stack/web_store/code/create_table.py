import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


user_table = 'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text,password text) '
cursor.execute(user_table)
item_table = 'CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text,price real) '
cursor.execute(item_table)

connection.commit()
connection.close()
