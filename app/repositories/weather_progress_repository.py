class WeatherProgressRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    # TODO: try catch
    def user_request_data_already_processed(self, uuid):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM progress WHERE user_request_id = ?", (uuid,)
        )
        return cursor.fetchone()[0]

    def request_uuid_exists(self, uuid):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM progress WHERE user_request_id = ?", (uuid,))
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            cursor.close()
