import aiohttp
import asyncio

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

    # TODO: review
    async def process(self, user_request_id, cities_id, units="metric"):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for city_id in cities_id:
                url = f"{self.weather_api_endpoint}?id={city_id}&appid={self.api_key}&units={units}"
                tasks.append(self.__fetch_city_weather_data(session, url, user_request_id))

                if len(tasks) >= self.limit:
                    results = await asyncio.gather(*tasks)
                    tasks = []  # Reset tasks
                    await asyncio.sleep(self.delay)

            if tasks:
                results = await asyncio.gather(*tasks)

    async def __fetch_city_weather_data(self, session, url, user_request_id):
        try:
            async with session.get(url, timeout=self.request_timeout) as response:
                if response.status == HTTPStatus.OK:
                    data = await response.json()
                    self.repository.store_weather_data_on_db(
                        user_request_id=user_request_id, data=data
                    )
                    return data
                else:
                    return {"error": f"Failed to retrieve weather data, status code: {response.status}"}
        except asyncio.TimeoutError:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
