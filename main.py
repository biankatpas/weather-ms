import tornado.ioloop
import tornado.web
import sqlite3

from decouple import config

from app.handlers import (
    WeatherRequestHandler,
    WeatherPercentageRequestHandler,
    IdRegisterRequestHandler
)

PORT = config("PORT", default=8888, cast=int)

def make_app():
    db_connection = sqlite3.connect('user_ids.db')
    db_connection.execute("CREATE TABLE IF NOT EXISTS user_ids (user_id TEXT UNIQUE)")

    return tornado.web.Application(
        [
           (r"/user/register", IdRegisterRequestHandler, dict(db_connection=db_connection)),
           (r"/weather", WeatherRequestHandler, dict(db_connection=db_connection)),
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
