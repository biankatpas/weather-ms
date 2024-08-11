import tornado.ioloop
import tornado.web

from app.handlers import (
    WeatherRequestHandler,
    WeatherPercentageRequestHandler
)

PORT = 8888

def make_app():
    return tornado.web.Application(
        [
           (r"/weather", WeatherRequestHandler),
           (r"/weather/percentage", WeatherPercentageRequestHandler),
        ],
        debug=True,
        autoreload=True
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print(f'Server is listening on port {PORT}')
    tornado.ioloop.IOLoop.current().start()
