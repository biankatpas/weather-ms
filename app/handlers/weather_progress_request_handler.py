import tornado.web

from http import HTTPStatus

from app.services.weather_progress_service import WeatherProgressService


class WeatherProgressRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection
        self.service = WeatherProgressService(self.db_connection)

    def get(self):
        user_request_id = self.get_query_argument("user_request_id", None)

        if not user_request_id:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "user_request_id field is required"})
            return

        progress_percentage = self.__get_progress_percentage(user_request_id)

        response = {
            "status": "success",
            "message": "weather progress percentage requested successfully",
            "data": {"progress_percentage": progress_percentage}
        }

        self.set_status(HTTPStatus.OK)
        self.write(response)

    def __get_progress_percentage(self, user_request_id):
        completed, total = self.service.get_progress_status(user_request_id)
        return (completed / total * 100) if total > 0 else 0
