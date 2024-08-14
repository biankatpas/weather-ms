import pytest
import uuid

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.services.request_service import RequestService


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
def request_service(db_connection):
    return RequestService(db_connection)


def test_service_store_request_uuid(request_service, db_connection):
    mock_uuid = str(uuid.uuid4())

    request_service.store_request_uuid(mock_uuid)

    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM request WHERE id = ?", (mock_uuid,))
    count = cursor.fetchone()[0]
    cursor.close()

    assert count == 1


def test_service_store_total_items(request_service, db_connection):
    mock_uuid = str(uuid.uuid4())
    mock_totals = 5

    request_service.store_request_uuid(mock_uuid)
    request_service.store_total_items(mock_uuid, mock_totals)

    cursor = db_connection.cursor()
    cursor.execute("SELECT total FROM request WHERE id = ?", (mock_uuid,))
    total = cursor.fetchone()[0]
    cursor.close()

    assert total == mock_totals


def test_service_request_uuid_exists(request_service, db_connection):
    mock_uuid = str(uuid.uuid4())

    request_service.store_request_uuid(mock_uuid)

    exists = request_service.request_uuid_exists(mock_uuid)

    assert exists


def test_service_request_uuid_not_exists(request_service):
    mock_uuid = str(uuid.uuid4())

    exists = request_service.request_uuid_exists(mock_uuid)

    assert not exists
