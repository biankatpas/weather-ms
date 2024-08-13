from app.repositories.weather_progress_repository import WeatherProgressRepository
from app.repositories.request_repository import RequestRepository


class WeatherProgressService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.weather_progress_repository = WeatherProgressRepository(self.db_connection)
        self.request_repository = RequestRepository(self.db_connection)

    # TODO: rename it
    def process(self, uuid):
        completed = self.weather_progress_repository.user_request_data_already_processed(uuid)
        total = self.request_repository.get_request_total_items_to_process(uuid)

        return completed, total

    def request_uuid_exists(self, uuid):
        return self.weather_progress_repository.request_uuid_exists(uuid)
