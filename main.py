import tornado.ioloop
import tornado.web

from decouple import config

from app.handlers import (
    WeatherRequestHandler,
    WeatherPercentageRequestHandler,
    IdRegisterRequestHandler
)

from app.core.database import initialize_db, get_db_connection

PORT = config("PORT", default=8888, cast=int)

initialize_db()

def make_app():
    db_connection = get_db_connection()

    return tornado.web.Application(
        [
           (r"/user/register", IdRegisterRequestHandler, dict(db_connection=db_connection)),
           (r"/weather", WeatherRequestHandler, dict(db_connection=db_connection)),
           (r"/weather/percentage", WeatherPercentageRequestHandler, dict(db_connection=db_connection)),
        ],
        debug=True,
        autoreload=True
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(PORT)
    print(f'Server is listening on port {PORT}')
    tornado.ioloop.IOLoop.current().start()
