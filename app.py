import json
import time
import sqlite3
import asyncio
from threading import Lock
from datetime import datetime
from flask import Flask, request, Response

from openWeatherApi import get_city_data

app = Flask(__name__)

#Rate limits
RATE_LIMIT = 60
TIME_WINDOW = 60 

#API calls management
request_times = []
lock = Lock()

@app.route('/', methods=['GET', 'POST'])
#Endpoints management
def app_home():
    if request.method == 'POST':
        user_id = request.args['user_id']
        user_id = int(user_id)
        request_date = datetime.now()
        if check_id(user_id):
             return Response ("This user id already exists.", status=501, mimetype='application/json')
        else:
            add_user(user_id)
            asyncio.run(get_openWeather_data(user_id, request_date))
            return '', 200
    elif request.method == 'GET':
        user_id = request.args['user_id']
        user_id = int(user_id)
        progress = get_progress(user_id)
        if progress:
            return (str(progress) + "%")
        else:
            return Response ("Id not found.", status=404, mimetype='application/json')

#Check if each request has an unique id
def check_id(user_id):
    with sqlite3.connect('flask-api.db') as connection:
        cur = connection.cursor()
        response = cur.execute("SELECT user_id FROM users WHERE user_id = " + str(user_id))
        response = response.fetchall()
    if response and user_id == response[0][0]:
        return True
    else:
        return False

#Add a new id on database
def add_user(user_id):
    with sqlite3.connect('flask-api.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO users (user_id) VALUES (?)",(user_id,))
        connection.commit()

#Call Open Weather API
async def get_openWeather_data(user_id, request_date):
    store_progress(user_id)
    cities_file = open('cities.txt','r') 
    cities = cities_file.readlines() 
    cities = cities[0].replace(',', '')
    cities = cities.split()

    data = []
    for city in cities:
        if allow_request():
            result = await get_city_data(city)
            result = result.json()
            temp = int(result["main"]["temp"])
            temp = temp - 273.15
            data.append({"city_id": city, "temperature": temp, "humidity": result["main"]["humidity"]})
            store_progress(user_id)
        else:
            wait_for_window()
            if allow_request():
                result = await get_city_data(city)
                result = result.json()
                temp = int(result["main"]["temp"])
                temp = temp - 273.15
                data.append({"city_id": city, "temperature": temp, "humidity": result["main"]["humidity"]})
                store_progress(user_id)
    data = json.dumps(data)
    store_data(data, user_id, request_date)

#Stores each request progress
def store_progress(user_id):
    with sqlite3.connect('flask-api.db') as connection:
        cur = connection.cursor()
        response = cur.execute("SELECT done FROM progress WHERE user_id = " + str(user_id))
        response = response.fetchall()
        if response:
            pgrs = response[0][0]
            pgrs = pgrs + (100/167)
            cur.execute("UPDATE progress SET done=? WHERE user_id = ?", (pgrs, user_id))
            connection.commit()
        else:
            cur.execute("INSERT INTO progress (user_id, done) VALUES (?,?)",(user_id, 0))
            connection.commit()

#Gets the progress(collected cities completed) for the given user id
def get_progress(user_id):
    with sqlite3.connect('flask-api.db') as connection:
        cur = connection.cursor()
        response = cur.execute("SELECT done FROM progress WHERE user_id = " + str(user_id))
        response = response.fetchall()
        if response:
            return response[0][0]
        else:
            return False

#Stores api request data on database
def store_data(data, user_id, request_date):
    with sqlite3.connect('flask-api.db') as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO requests (user_id, request_date, data) VALUES (?,?,?)",(user_id, request_date, data))
        connection.commit()

def allow_request():
    global request_times
    with lock:
        new_times = []
        current_time = time.time()
        for t in request_times:
            new_time = current_time - t
            if new_time < TIME_WINDOW:
                new_times.append(t)
        request_times = new_times
        if len(request_times) < RATE_LIMIT:
            request_times.append(current_time)
            return True
        else:
            return False
        
def wait_for_window():
    with lock:
        if len(request_times) == 0:
            return

        current_time = time.time()
        sleep_time = TIME_WINDOW - (current_time - request_times[0])
        
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == '__main__':
    app.run(port=32187, debug=True, use_reloader=True, host='0.0.0.0')