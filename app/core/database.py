import sqlite3


def get_db_connection():
    conn = sqlite3.connect('weather_ms.db')
    return conn

def initialize_db():
    conn = get_db_connection()
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS user (id TEXT UNIQUE)")
        # TODO: temperature, humidity, city id -> json
        # TODO: add request_datetime
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                request_uuid TEXT,
                user_id TEXT,
                city_id INTEGER,
                temperature REAL,
                humidity REAL,
                PRIMARY KEY (request_uuid, city_id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
    conn.close()
