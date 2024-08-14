import pytest

import tornado.escape
import tornado.testing

from tornado.web import Application
from unittest.mock import MagicMock

from app.handlers.weather_progress_request_handler import WeatherProgressRequestHandler
from app.repositories.weather_repository import WeatherRepository
from app.repositories.weather_progress_repository import WeatherProgressRepository
from app.repositories.request_repository import RequestRepository
from app.services.weather_progress_service import WeatherProgressService
from app.core.database import get_db_connection, initialize_db


@pytest.fixture
def db_connection():
    initialize_db()
    conn = get_db_connection()
    yield conn
    conn.close()

class TestWeatherProgressRequestHandler(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return Application([
            (r"/weather-progress", WeatherProgressRequestHandler, dict(db_connection=db_connection)),
        ])

    def setUp(self):
        super().setUp()
        self.db_connection = db_connection
        self.weather_repository = WeatherRepository(self.db_connection)
        self.weather_progress_repository = WeatherProgressRepository(self.db_connection)
        self.request_repository = RequestRepository(self.db_connection)
        self.weather_progress_service = WeatherProgressService(self.db_connection)

        self.weather_repository.store_weather_data_on_db = MagicMock()
        self.request_repository.get_request_total_items_to_process = MagicMock(return_value=10)
        self.weather_progress_repository.user_request_data_already_processed = MagicMock(return_value=5)

    def test_get_progress_status_no_request_id(self):
        response = self.fetch("/weather-progress", method="GET")

        response_json = tornado.escape.json_decode(response.body)

        self.assertEqual(response.code, 400)
        self.assertEqual(response_json["error"], "user_request_id field is required")

    # TODO
    # def test_get_progress_status_success(self):
    #     mock_uuid = "test-uuid"

    #     self.request_repository.store_request_uuid_to_process(mock_uuid)
    #     self.request_repository.store_request_total_items_to_process(mock_uuid, 10)

    #     self.weather_repository.store_weather_data_on_db(
    #         mock_uuid,
    #         {
    #             'id': 123,
    #             'main': {
    #                 'temp': 25.5,
    #                 'humidity': 60
    #             }
    #         }
    #     )

    #     response = self.fetch(f"/weather-progress?user_request_id={mock_uuid}", method="GET")

    #     response_json = tornado.escape.json_decode(response.body)

    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response_json["status"], "success")
    #     self.assertEqual(response_json["message"], "weather progress percentage requested successfully")
