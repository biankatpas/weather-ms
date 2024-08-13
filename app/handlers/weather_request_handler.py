import tornado.web
import tornado.escape

from http import HTTPStatus
from decouple import config

from app.services.request_service import RequestService
from app.services.weather_service import WeatherService
from app.services.weather_progress_service import WeatherProgressService
from app.utils.csv_utils import read_cities_ids_from_csv


class WeatherRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection
        self.cities_file_path = config('CITIES_FILE_PATH', default="app/resources/cities_id_list.csv")
        self.request_service = RequestService(self.db_connection)
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

        request_uuid_exists = self.request_service.request_uuid_exists(user_request_id)
        if not request_uuid_exists:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write({"error": "user_request_id does not exist, please generate one"})
            return

        request_uuid_in_progress = self.weather_progress_service.request_uuid_exists(user_request_id)
        if request_uuid_in_progress:
            self.set_status(HTTPStatus.CONFLICT)
            self.write({"error": "user_request_id already used, please generate a new one"})
            return

        cities_id = read_cities_ids_from_csv(
            file_path=self.cities_file_path
        )

        self.request_service.store_total_items(
            uuid=user_request_id,
            totals=len(cities_id)
        )

        weather_data = await self.weather_service.fetch_cities_weather_data(
            uuid=user_request_id,
            cities_id=cities_id
        )

        weather_response = self.__format_weather_data(weather_data)

        response = {
            "status": "success",
            "message": "weather data requested successfully",
            "data": weather_response
        }

        self.status_code = HTTPStatus.OK

        self.write(response)

    def __format_weather_data(self, weather_data):
        weather_response = []
        for data in weather_data:
            city_id = data.get('id')
            temperature = data.get('main', {}).get('temp')
            humidity = data.get('main', {}).get('humidity')

            weather_response.append({
                "city_id": city_id,
                "temperature": temperature,
                "humidity": humidity
            })

        return weather_response
