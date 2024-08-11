import tornado.web

from app.services.weather_service import WeatherService


class WeatherRequestHandler(tornado.web.RequestHandler):

    def post(self):
        self.write("weather")
