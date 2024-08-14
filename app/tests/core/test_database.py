import sqlite3
import os
import pytest
from io import StringIO
from app.core.database import get_db_connection, initialize_db


def test_get_db_connection():
    conn = get_db_connection()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_initialize_db():
    initialize_db()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(request);")
    request_table_info = cursor.fetchall()
    assert len(request_table_info) == 2

    cursor.execute("PRAGMA table_info(progress);")
    progress_table_info = cursor.fetchall()
    assert len(progress_table_info) == 4

    conn.close()

    if os.path.exists('weather_ms.db'):
        os.remove('weather_ms.db')
