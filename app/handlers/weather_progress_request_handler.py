from http import HTTPStatus

import tornado.web

from app.services.weather_service import WeatherService


class WeatherProgressRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection
        self.service = WeatherService(self.db_connection)

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

        # TODO: implement DB access code in progress_repository.py
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM progress WHERE user_request_id = ?", (user_request_id,)
        )
        completed = cursor.fetchone()[0]

        # TODO: get total from cities id list
        mock_total = 167
        total = mock_total

        progress_percentage = (completed / total * 100) if total > 0 else 0

        response = {
            "user_request_id": user_request_id,
            "progress_percentage": progress_percentage
        }
        self.set_status(HTTPStatus.OK)
        self.write(response)
