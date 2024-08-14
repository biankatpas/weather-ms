import uuid
import json
import pytest

from app.fixtures.database_fixture import get_db_connection, initialize_db
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


@pytest.fixture
def weather_repository(db_connection):
    return WeatherRepository(db_connection)


def test_store_weather_data_on_db_success(weather_repository, db_connection):
    mock_uuid = str(uuid.uuid4())
    mock_data = {
        'id': 123,
        'main': {
            'temp': 25.5,
            'humidity': 60
        }
    }

    weather_repository.store_weather_data_on_db(mock_uuid, mock_data)

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM progress WHERE user_request_id = ?", (mock_uuid,))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[1] == mock_uuid
    assert result[2] is not None
    assert result[2] == json.dumps({
        "city_id": mock_data['id'],
        "temperature": mock_data['main']['temp'],
        "humidity": mock_data['main']['humidity']
    })
