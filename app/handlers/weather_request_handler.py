import tornado.web
import tornado.escape

from http import HTTPStatus

from app.services.weather_service import WeatherService
from app.services.weather_progress_service import WeatherProgressService
from app.utils.csv_utils import read_cities_ids_from_csv


class WeatherRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection

        self.weather_service = WeatherService(self.db_connection)
        self.weather_progress_service = WeatherProgressService(self.db_connection)

    async def post(self):
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
            self.write(
                {"error": "user_request_id field is required"}
            )
            return

        request_uuid_exists = self.weather_service.request_uuid_exists(user_request_id)
        if not request_uuid_exists:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write({"error": "user_request_id does not exist"})
            return

        request_uuid_in_progress = self.weather_progress_service.request_uuid_exists(user_request_id)
        if request_uuid_in_progress:
            self.set_status(HTTPStatus.CONFLICT)
            self.write({"error": "user_request_id already exists. Please generate a new ID."})
            return

        # TODO: get file path from request body
        cities_id = read_cities_ids_from_csv(file_path="app/resources/cities_id_list.csv")

        # TODO: save total items to process in request table

        # TODO: return weather data
        _ = await self.weather_service.fetch_cities_weather_data(
            user_request_id=user_request_id,
            cities_id=cities_id
        )

        response = {
            "status": "success",
            "message": "weather data requested successfully",
            "data": {}
        }

        self.status_code = HTTPStatus.OK

        self.write(response)
