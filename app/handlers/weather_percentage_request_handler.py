from http import HTTPStatus

import tornado.web

from app.services.weather_service import WeatherService


class WeatherPercentageRequestHandler(tornado.web.RequestHandler):
    # TODO: WIP
    def get(self):
        pass
