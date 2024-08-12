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
            request_uuid = request_data.get("request_uuid")
        except ValueError as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Invalid JSON", "message": str(e)})
            return

        if not request_uuid:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Request UUID is required"})
            return

        # TODO: implement DB access code in progress_repository.py
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM progress WHERE request_uuid = ?", (request_uuid,)
        )
        completed = cursor.fetchone()[0]

        # TODO: get total from cities id list
        mock_total = 167
        total = mock_total

        progress_percentage = (completed / total * 100) if total > 0 else 0

        response = {
            "request_id": request_uuid,
            "progress_percentage": progress_percentage
        }
        self.set_status(HTTPStatus.OK)
        self.write(response)
