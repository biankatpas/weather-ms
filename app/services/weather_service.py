import tornado.httpclient
import pandas as pd
import json
import asyncio

from decouple import config


class WeatherService():
    def __init__(self):
        self.api_key = config('API_KEY')

    def get_weather_by_cities_id(self, cities_id):
        pass
