from app.repositories.weather_progress_repository import WeatherProgressRepository
from app.repositories.request_repository import RequestRepository


class WeatherProgressService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.weather_progress_repository = WeatherProgressRepository(self.db_connection)
        self.request_repository = RequestRepository(self.db_connection)

    def process(self, user_request_id):
        completed = self.weather_progress_repository.user_request_data_already_processed(user_request_id)
        total = self.request_repository.get_request_total_items_to_process(user_request_id)

        return completed, total

    def request_uuid_exists(self, user_request_id):
        return self.weather_progress_repository.request_uuid_exists(user_request_id)
