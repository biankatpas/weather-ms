import uuid
import sqlite3
import pytest

from app.fixtures.database_fixture import get_db_connection, initialize_db
from app.repositories.request_repository import RequestRepository


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
def request_repository(db_connection):
    return RequestRepository(db_connection)


def test_store_request_uuid_to_process_success(request_repository):
    mock_uuid = str(uuid.uuid4())

    request_repository.store_request_uuid_to_process(mock_uuid)

    cursor = request_repository.db_connection.cursor()
    cursor.execute("SELECT id FROM request WHERE id = ?", (mock_uuid,))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == mock_uuid


def test_store_request_uuid_to_process_unique(request_repository):
    mock_uuid = str(uuid.uuid4())

    request_repository.store_request_uuid_to_process(mock_uuid)
    request_repository.store_request_uuid_to_process(mock_uuid)

    cursor = request_repository.db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM request WHERE id = ?", (mock_uuid,))
    count = cursor.fetchone()[0]
    cursor.close()

    assert count == 1


def test_store_request_total_items_to_process_update_existing(request_repository):
    mock_uuid = str(uuid.uuid4())
    new_total = 10

    request_repository.store_request_uuid_to_process(mock_uuid)
    request_repository.store_request_total_items_to_process(mock_uuid, new_total)

    cursor = request_repository.db_connection.cursor()
    cursor.execute("SELECT total FROM request WHERE id = ?", (mock_uuid,))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == new_total


def test_store_request_total_items_to_process_insert_new(request_repository):
    mock_uuid = str(uuid.uuid4())
    total = 167

    request_repository.store_request_total_items_to_process(mock_uuid, total)

    cursor = request_repository.db_connection.cursor()
    cursor.execute("SELECT total FROM request WHERE id = ?", (mock_uuid,))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == total


def test_request_uuid_exists_when_uuid_present(request_repository):
    mock_uuid = str(uuid.uuid4())

    request_repository.store_request_uuid_to_process(mock_uuid)

    exists = request_repository.request_uuid_exists(mock_uuid)

    assert exists is True


def test_request_uuid_exists_when_uuid_not_present(request_repository):
    mock_uuid = str(uuid.uuid4())

    exists = request_repository.request_uuid_exists(mock_uuid)

    assert exists is False


def test_get_request_total_items_to_process_when_uuid_present_with_total(request_repository):
    mock_uuid = str(uuid.uuid4())
    mock_total = 42

    request_repository.store_request_total_items_to_process(mock_uuid, mock_total)

    retrieved_total = request_repository.get_request_total_items_to_process(mock_uuid)

    assert retrieved_total == mock_total


def test_get_request_total_items_to_process_when_uuid_present_with_null_total(request_repository):
    mock_uuid = str(uuid.uuid4())

    request_repository.store_request_total_items_to_process(mock_uuid, None)

    retrieved_total = request_repository.get_request_total_items_to_process(mock_uuid)

    assert retrieved_total == 0


def test_get_request_total_items_to_process_when_uuid_not_present(request_repository):
    mock_uuid = str(uuid.uuid4())

    retrieved_total = request_repository.get_request_total_items_to_process(mock_uuid)

    assert retrieved_total == 0
