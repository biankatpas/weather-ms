import sqlite3


def get_db_connection():
    conn = sqlite3.connect('weather_ms.db')
    return conn

def initialize_db():
    conn = get_db_connection()
    with conn:
        conn.execute("CREATE TABLE IF NOT EXISTS user (id TEXT UNIQUE)")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_request_id TEXT,
                weather_data TEXT,
                request_datetime TEXT,
                FOREIGN KEY (user_request_id) REFERENCES user(id)
            )
        """)
    conn.close()
