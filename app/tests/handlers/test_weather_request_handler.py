import uuid
import pytest
import json
import pytest_asyncio
import tornado.escape

from unittest.mock import MagicMock, patch, AsyncMock

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase, gen_test

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.handlers.weather_request_handler import WeatherRequestHandler
from app.repositories.request_repository import RequestRepository
from app.repositories.weather_repository import WeatherRepository
from app.services.weather_service import WeatherService


class WeatherRequestHandlerTestCase1(AsyncHTTPTestCase):

    def get_app(self):
        self.mock_cursor = MagicMock()
        self.mock_db_connection = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_cursor

        return Application([
            (r"/weather", WeatherRequestHandler, dict(db_connection=self.mock_db_connection)),
        ])

    @gen_test
    async def test_post_no_request_id(self):
        invalid_body = {}

        response = await self.http_client.fetch(
            self.get_url("/weather"),
            method='POST',
            body=json.dumps(invalid_body),
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 400
        assert response_json['error'] == "user_request_id field is required"


    @gen_test
    async def test_post_uuid_does_not_exist(self):
        mock_uuid = str(uuid.uuid4())
        valid_body = {"user_request_id": mock_uuid}

        response = await self.http_client.fetch(
            self.get_url(f"/weather"),
            method="POST",
            body=json.dumps(valid_body),
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 404
        assert response_json['error'] == 'user_request_id does not exist, please generate one'


class WeatherRequestHandlerTestCase2(AsyncHTTPTestCase):
    def get_app(self):
        initialize_db()
        self.db_connection = get_db_connection()
        return Application([
            (r"/weather", WeatherRequestHandler, dict(db_connection=self.db_connection)),
        ])

    @gen_test
    @patch.object(WeatherService, 'fetch_cities_weather_data', new_callable=AsyncMock)
    @patch.object(WeatherRequestHandler, '_WeatherRequestHandler__format_weather_data', new_callable=MagicMock)
    async def test_post_success(self, mock_fetch_cities_weather_data, mock_format_weather_data):
        mock_uuid = str(uuid.uuid4())

        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO request (id) VALUES (?)", (mock_uuid,))
        self.db_connection.commit()
        cursor.close()

        valid_body = {"user_request_id": mock_uuid}

        mock_fetch_cities_weather_data.return_value = {
            "city_id_1": {
                "temperature": 22.5,
                "humidity": 55
            },
            "city_id_2": {
                "temperature": 18.0,
                "humidity": 60
            }
        }

        mock_format_weather_data.return_value = {
            "status": "success",
            "message": "weather data requested successfully",
            "data": [
                {"city_id": "city_id_1", "temperature": 22.5, "humidity": 55},
                {"city_id": "city_id_2", "temperature": 18.0, "humidity": 60}
            ]
        }

        response = await self.http_client.fetch(
            self.get_url(f"/weather"),
            method="POST",
            body=json.dumps(valid_body),
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 200
        assert response_json['status'] == "success"
        assert len(response_json['data']) == 2
