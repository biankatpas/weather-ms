import json

from datetime import datetime


class WeatherRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_weather_data_on_db(self, uuid, data):
        try:
            cursor = self.db_connection.cursor()
            request_datetime = datetime.utcnow().isoformat()

            item = {
                "city_id": data['id'],
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity']
            }

            weather_data_json = json.dumps(item)

            cursor.execute(
                "INSERT INTO progress (user_request_id, weather_data, request_datetime) VALUES (?, ?, ?)",
                (uuid, weather_data_json, request_datetime)
            )

            self.db_connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()

        finally:
            cursor.close()
