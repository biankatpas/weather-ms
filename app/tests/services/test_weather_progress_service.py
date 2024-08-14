import pytest
import uuid

from app.fixtures.database_fixture import get_db_connection, initialize_db

from app.repositories.weather_repository import WeatherRepository
from app.repositories.weather_progress_repository import WeatherProgressRepository
from app.repositories.request_repository import RequestRepository
from app.services.weather_progress_service import WeatherProgressService


@pytest.fixture
def db_connection():
    initialize_db()
    conn = get_db_connection()
    yield conn
    conn.close()

    import os
    if os.path.exists('app/tests/weather_ms.db'):
        os.remove('app/tests/weather_ms.db')


@pytest.fixture
def weather_progress_service(db_connection):
    return WeatherProgressService(db_connection)


def test_service_get_progress_status(weather_progress_service, db_connection):
    mock_uuid = str(uuid.uuid4())
    mock_totals = 10

    request_repository = RequestRepository(db_connection)
    weather_repository = WeatherRepository(db_connection)
    weather_progress_repository = WeatherProgressRepository(db_connection)

    request_repository.store_request_uuid_to_process(mock_uuid)
    request_repository.store_request_total_items_to_process(mock_uuid, mock_totals)

    mock_weather_data = {
        'id': 123,
        'main': {
            'temp': 25.5,
            'humidity': 60
        }
    }

    weather_repository.store_weather_data_on_db(mock_uuid, mock_weather_data)

    completed = weather_progress_repository.user_request_data_already_processed(mock_uuid)

    result_completed, result_total = weather_progress_service.get_progress_status(mock_uuid)
    assert result_completed == completed
    assert result_total == mock_totals


def test_service_request_uuid_exists(weather_progress_service, db_connection):
    mock_uuid = str(uuid.uuid4())
    mock_weather_data = {
        'id': 123,
        'main': {
            'temp': 25.5,
            'humidity': 60
        }
    }

    request_repository = RequestRepository(db_connection)
    request_repository.store_request_uuid_to_process(mock_uuid)

    weather_repository = WeatherRepository(db_connection)
    weather_repository.store_weather_data_on_db(mock_uuid, mock_weather_data)

    exists = weather_progress_service.request_uuid_exists(mock_uuid)

    assert exists


def test_service_request_uuid_not_exists(weather_progress_service):
    mock_uuid = str(uuid.uuid4())

    exists = weather_progress_service.request_uuid_exists(mock_uuid)

    assert not exists
