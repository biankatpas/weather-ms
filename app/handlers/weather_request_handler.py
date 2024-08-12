import uuid
import tornado.web
import tornado.escape

from http import HTTPStatus

from app.services.weather_service import WeatherService
from app.storage.weather_storage import WeatherStorage
from app.utils.csv_utils import read_cities_ids_from_csv


class WeatherRequestHandler(tornado.web.RequestHandler):
    def initialize(self, db_connection):
        self.db_connection = db_connection
        self.storage = WeatherStorage(db_connection)
        self.service = WeatherService()

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

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE id = ?", (user_id,))
        exists = cursor.fetchone()[0]

        if not exists:
            self.set_status(HTTPStatus.NOT_FOUND)
            self.write({"error": "User ID does not exist"})
            return

        request_uuid = str(uuid.uuid4())
        # TODO: get file path from request body
        cities_id = read_cities_ids_from_csv(file_path="app/resources/cities_id_list.csv")

        weather_data = await self.service.get_weather_by_cities_id(
            cities_id=cities_id
        )

        self.storage.store_weather_data_as_json(
            user_id=user_id, request_uuid=request_uuid, data=weather_data
        )

        response = {
            "status": "success",
            "message": "Weather data requested successfully",
            "request_id": request_uuid
        }
        self.status_code = HTTPStatus.OK
        self.write(response)
