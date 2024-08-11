from http import HTTPStatus
import tornado.web

from app.services.weather_service import WeatherService


class WeatherRequestHandler(tornado.web.RequestHandler):

    async def post(self):
        if not self.request.body:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Request body cannot be empty"})
            return

        request_body = self.request.body.decode('utf-8')
        try:
            request_data = tornado.escape.json_decode(request_body)
            user_id = request_data.get("user_id")
        except ValueError as e:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "Invalid JSON", "message": str(e)})
            return

        if not user_id:
            self.set_status(HTTPStatus.BAD_REQUEST)
            self.write({"error": "User ID is required"})
            return
