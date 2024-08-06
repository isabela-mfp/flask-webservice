import os
import asyncio
import requests

apikey = os.getenv("API_TOKEN")

async def get_city_data(city_id):
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, requests.get, 'https://api.openweathermap.org/data/2.5/weather?id=' + str(city_id) + '&appid=' + str(apikey))
    return r