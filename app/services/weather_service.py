import aiohttp
import asyncio
import json

from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.web import Application

from decouple import config
from http import HTTPStatus

from app.repositories.weather_repository import WeatherRepository

class WeatherService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.repository = WeatherRepository(self.db_connection)

        self.api_key = config('API_KEY')
        self.weather_api_endpoint = config('WEATHER_API_ENDPOINT')

        self.limit = 60
        self.delay = 60
        self.request_timeout = 10

    async def process(self, request_uuid, user_id, cities_id, units="metric"):
        weather_data = await self.__fetch_cities_weather_data(cities_id, units)

        self.repository.store_weather_data_on_db(
            user_id=user_id, request_uuid=request_uuid, data=weather_data
        )

        return weather_data

    async def __fetch_cities_weather_data(self, cities_id, units):
        all_weather_data = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for city_id in cities_id:
                url = f"{self.weather_api_endpoint}?id={city_id}&appid={self.api_key}&units={units}"
                tasks.append(self.__fetch_city_weather_data(session, url))

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

    async def __fetch_city_weather_data(self, session, url):
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
