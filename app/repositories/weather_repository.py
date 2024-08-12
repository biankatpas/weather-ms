class WeatherRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_weather_data_on_db(self, user_request_id, data):
        try:
            cursor = self.db_connection.cursor()

            item = {
                "city_id": data['id'],
                "temperature": data['main']['temp'],
                "humidity": data['main']['humidity']
            }

            cursor.execute(
                "INSERT INTO progress (user_request_id, city_id, temperature, humidity) VALUES (?, ?, ?, ?)",
                (user_request_id, item['city_id'], item['temperature'], item['humidity'])
            )

            self.db_connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()

        finally:
            cursor.close()
