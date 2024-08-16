import pytest
import pytest_asyncio
import tornado.escape

from unittest.mock import MagicMock, patch
from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.handlers.weather_progress_request_handler import WeatherProgressRequestHandler
from app.repositories.request_repository import RequestRepository
from app.repositories.weather_repository import WeatherRepository


@pytest.fixture
def db_connection():
    initialize_db()
    conn = get_db_connection()
    yield conn
    conn.close()

    import os
    if os.path.exists('app/tests/weather_ms.db'):
        os.remove('app/tests/weather_ms.db')


class WeatherProgressRequestHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        self.mock_cursor = MagicMock()
        self.mock_db_connection = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_cursor

        return Application([
            (r"/weather/progress", WeatherProgressRequestHandler, dict(db_connection=self.mock_db_connection)),
        ])

    @gen_test
    async def test_get_progress_status_no_request_id(self):
        response = await self.http_client.fetch(
            self.get_url("/weather/progress"),
            method='GET',
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 400
        assert response_json['error'] == "user_request_id field is required"


    @gen_test
    async def test_get_progress_status_success(self):
        mock_uuid = "test-uuid"

        self.mock_cursor.fetchone.return_value = [1]
        self.mock_cursor.rowcount = 1

        request_repository = RequestRepository(self.mock_db_connection)
        request_repository.store_request_uuid_to_process(mock_uuid)
        request_repository.store_request_total_items_to_process(mock_uuid, 1)

        weather_repository = MagicMock()
        weather_repository.store_weather_data_on_db.return_value = None

        weather_repository.store_weather_data_on_db(
            mock_uuid,
            {
                'id': 123,
                'main': {
                    'temp': 25.5,
                    'humidity': 60
                }
            }
        )

        response = await self.http_client.fetch(
            self.get_url(f"/weather/progress?user_request_id={mock_uuid}"),
            method="GET",
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 200
        assert "progress_percentage" in response_json["data"]
