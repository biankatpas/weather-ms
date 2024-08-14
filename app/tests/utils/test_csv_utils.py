import pytest
import pandas as pd
from io import StringIO
from app.utils.csv_utils import read_cities_ids_from_csv


def test_read_cities_ids_from_csv():
    mock_csv_data = StringIO("""
    1
    2
    3
    4
    """)

    expected_ids = [1, 2, 3, 4]

    ids = read_cities_ids_from_csv(mock_csv_data)

    assert ids == expected_ids


def test_read_cities_ids_from_csv_with_non_numeric_values():
    mock_csv_data = StringIO("""
    1
    a
    3
    4
    """)

    expected_ids = [1, 3, 4]

    ids = read_cities_ids_from_csv(mock_csv_data)

    assert ids == expected_ids


def test_read_cities_ids_from_csv_empty():
    mock_csv_data = StringIO("")

    expected_ids = []

    ids = read_cities_ids_from_csv(mock_csv_data)

    assert ids == expected_ids
