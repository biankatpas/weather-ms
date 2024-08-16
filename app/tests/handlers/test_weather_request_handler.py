import uuid
import pytest
import json
import pytest_asyncio
import tornado.escape

from unittest.mock import MagicMock, patch
from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase
from tornado.testing import gen_test

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.handlers.weather_request_handler import WeatherRequestHandler
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


class WeatherRequestHandlerTestCase(AsyncHTTPTestCase):

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
