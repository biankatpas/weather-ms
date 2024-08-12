class WeatherStorage:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_weather_data_as_json(self, request_uuid, user_id, data):
        try:
            cursor = self.db_connection.cursor()

            for city_data in data:
                item = {
                    "city_id": city_data['id'],
                    "temperature": city_data['main']['temp'],
                    "humidity": city_data['main']['humidity']
                }

                cursor.execute("INSERT INTO progress (request_uuid, user_id, city_id, temperature, humidity) VALUES (?, ?, ?, ?, ?)",
                               (request_uuid, user_id, item['city_id'], item['temperature'], item['humidity']))

            self.db_connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()

        finally:
            cursor.close()
