import tornado.web
from app.services.weather_service import WeatherService


class WeatherRequestHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, I'm running!")
