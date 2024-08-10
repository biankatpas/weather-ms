import tornado.ioloop
import tornado.web
from app.handlers.weather_request_handler import WeatherRequestHandler

def make_app():
    return tornado.web.Application([
        (r"/weather-ms", WeatherRequestHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
