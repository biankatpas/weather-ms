class WeatherProgressRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def user_request_data_already_processed(self, user_request_id):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM progress WHERE user_request_id = ?", (user_request_id,)
        )
        return cursor.fetchone()[0]
