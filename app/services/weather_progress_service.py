from app.repositories.weather_progress_repository import WeatherProgressRepository
from app.repositories.user_repository import UserRepository


class WeatherProgressService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.weather_progress_repository = WeatherProgressRepository(self.db_connection)
        self.user_repository = UserRepository(self.db_connection)

    def process(self, user_request_id):
        completed = self.weather_progress_repository.user_request_data_already_processed(user_request_id)
        total = self.user_repository.get_request_total_items_to_process(user_request_id)

        return completed, total

