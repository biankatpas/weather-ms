from app.repositories.weather_progress_repository import WeatherProgressRepository


class WeatherProgressService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.repository = WeatherProgressRepository(self.db_connection)

    def process(self, user_request_id):
        return self.repository.user_request_data_already_processed(user_request_id)
