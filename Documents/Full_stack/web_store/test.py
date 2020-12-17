import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users(id int, username text,password text)"
cursor.execute(create_table)

user = (1, 'mazina', 'mazina')
insert_user = "INSERT INTO users VALUES(?,?,?)"
cursor.execute(insert_user, user)

users = [(2, 'davy', 'davy'), (3, 'arcel', 'arcel')]
insert_user = "INSERT INTO users VALUES(?,?,?)"
cursor.executemany(insert_user, users)

select_query = 'SELECT * FROM users'
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
