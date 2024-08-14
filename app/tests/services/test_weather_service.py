import pytest
import asyncio
from aioresponses import aioresponses
from unittest.mock import MagicMock

from decouple import config
from app.services.weather_service import WeatherService

API_KEY = config('API_KEY')
WEATHER_API_ENDPOINT = config('WEATHER_API_ENDPOINT')

@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def weather_service(mock_db_connection):
    weather_service = WeatherService(mock_db_connection)
    weather_service.repository = MagicMock()
    return weather_service

@pytest.mark.asyncio
async def test_fetch_cities_weather_data(weather_service):
    weather_service.repository.store_weather_data_on_db = MagicMock()

    with aioresponses() as mocked:
        mock_response = {
            "id": 123,
            "name": "Test City",
            "main": {
                "temp": 20,
                "humidity": 50
            }
        }

        url = f"{WEATHER_API_ENDPOINT}?id=123&appid={API_KEY}&units=metric"
        mocked.get(url, payload=mock_response, status=200)

        uuid = "test-uuid"
        cities_id = [123]

        _ = await weather_service.fetch_cities_weather_data(uuid, cities_id)
        assert weather_service.repository.store_weather_data_on_db.called
