import aiohttp
import asyncio
import json

from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.web import Application

from decouple import config
from http import HTTPStatus

class WeatherService:
    def __init__(self):
        self.api_key = config('API_KEY')
        self.weather_api_endpoint = config('WEATHER_API_ENDPOINT')
        self.limit = 60
        self.delay = 60
        self.request_timeout = 10

    async def get_weather_by_cities_id(self, cities_id, units="metric"):
        all_weather_data = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for city_id in cities_id:
                url = f"{self.weather_api_endpoint}?id={city_id}&appid={self.api_key}&units={units}"
                tasks.append(self.__fetch_weather_data(session, url))

                # Ensure the rate limit of 60 requests per minute
                if len(tasks) >= self.limit:
                    # Run tasks and wait for their completion
                    results = await asyncio.gather(*tasks)
                    all_weather_data.extend(results)
                    tasks = []  # Reset tasks
                    await asyncio.sleep(self.delay)

            # Fetch remaining tasks
            if tasks:
                results = await asyncio.gather(*tasks)
                all_weather_data.extend(results)

        return all_weather_data

    async def __fetch_weather_data(self, session, url):
        try:
            async with session.get(url, timeout=self.request_timeout) as response:
                if response.status == HTTPStatus.OK:
                    data = await response.json()
                    return data
                else:
                    return {"error": f"Failed to retrieve weather data, status code: {response.status}"}
        except asyncio.TimeoutError:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
