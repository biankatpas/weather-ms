import tornado.escape
import tornado.testing

from tornado.testing import gen_test, AsyncHTTPTestCase
from tornado.web import Application
from unittest.mock import MagicMock

from app.handlers.id_register_request_handler import IdRegisterRequestHandler


class IdRegisterRequestHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        self.mock_cursor = MagicMock()
        self.mock_db_connection = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_cursor

        return Application([
            (r"/user/register", IdRegisterRequestHandler, dict(db_connection=self.mock_db_connection)),
        ])

    @gen_test
    async def test_post_no_request_id(self):
        response = await self.http_client.fetch(
            self.get_url("/user/register"),
            method='POST',
            body="",
            raise_error=False
        )

        response_json = tornado.escape.json_decode(response.body)

        assert response.code == 200
        assert response_json['message'] == "user request id registered successfully"
