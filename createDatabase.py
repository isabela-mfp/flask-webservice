import sqlite3

connection = sqlite3.connect('flask-api.db')
connection.execute('CREATE TABLE users (user_id INTEGER)')
connection.execute('CREATE TABLE requests (user_id INTEGER, request_date TEXT, data TEXT)')
connection.execute('CREATE TABLE progress (user_id INTEGER, done REAL)')
connection.close()