from http import HTTPStatus

import tornado.web

from app.services.weather_progress_service import WeatherProgressService


class WeatherProgressRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection
        self.service = WeatherProgressService(self.db_connection)

    def get(self):
        if not self.request.body:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Request body cannot be empty"})
            return

        request_body = self.request.body.decode('utf-8')
        try:
            request_data = tornado.escape.json_decode(request_body)
            user_request_id = request_data.get("user_request_id")
        except ValueError as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Invalid JSON", "message": str(e)})
            return

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
        completed, total = self.service.process(user_request_id)

        return (completed / total * 100) if total > 0 else 0
