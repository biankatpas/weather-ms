from http import HTTPStatus

import tornado.web

from app.services.weather_service import WeatherService


class WeatherPercentageRequestHandler(tornado.web.RequestHandler):

    def get(self):
        pass
