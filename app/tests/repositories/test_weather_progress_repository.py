import pytest
import uuid

from datetime import datetime

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.repositories.weather_progress_repository import WeatherProgressRepository


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
def weather_progress_repository(db_connection):
    return WeatherProgressRepository(db_connection)


def test_user_request_data_already_processed_success(weather_progress_repository, db_connection):
    mock_uuid = str(uuid.uuid4())

    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO progress (user_request_id, weather_data, request_datetime) VALUES (?, ?, ?)",
        (mock_uuid, '{"city_id": 123, "temperature": 25.5, "humidity": 60}', datetime.utcnow().isoformat())
    )
    db_connection.commit()

    count = weather_progress_repository.user_request_data_already_processed(mock_uuid)
    cursor.close()

    assert count == 1


def test_user_request_data_already_processed_no_data(weather_progress_repository):
    mock_uuid = str(uuid.uuid4())

    count = weather_progress_repository.user_request_data_already_processed(mock_uuid)

    assert count == 0


def test_request_uuid_exists(weather_progress_repository, db_connection):
    mock_uuid = str(uuid.uuid4())

    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO progress (user_request_id, weather_data, request_datetime) VALUES (?, ?, ?)",
        (mock_uuid, '{"city_id": 123, "temperature": 25.5, "humidity": 60}', datetime.utcnow().isoformat())
    )
    db_connection.commit()

    exists = weather_progress_repository.request_uuid_exists(mock_uuid)
    cursor.close()

    assert exists


def test_request_uuid_do_not_exists(weather_progress_repository):
    mock_uuid = str(uuid.uuid4())

    exists = weather_progress_repository.request_uuid_exists(mock_uuid)

    assert not exists
