import uuid
import pytest

import tornado.escape
import tornado.testing

from tornado.web import Application
from unittest.mock import MagicMock

from app.handlers.id_register_request_handler import IdRegisterRequestHandler
from app.services.request_service import RequestService
from app.core.database import get_db_connection, initialize_db


class TestIdRegisterRequestHandler(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        initialize_db()
        self.db_connection = get_db_connection()
        self.request_service = RequestService(self.db_connection)
        self.request_service.store_request_uuid = MagicMock()
        return Application([
            (r"/user-register", IdRegisterRequestHandler, dict(db_connection=self.db_connection)),
        ])
    
    # TODO:
    # async def test_post_register_id(self):
    #     response = await self.fetch("/register-id", method="POST")
    #     response_json = tornado.escape.json_decode(response.body)

    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response_json["status"], "success")
    #     self.assertEqual(response_json["message"], "user request id registered successfully")
    #     self.assertIn("user_request_id", response_json["data"])

    #     self.request_service.store_request_uuid.assert_called_once()
    #     self.assertTrue(uuid.UUID(self.request_service.store_request_uuid.call_args[0][0]))

    def tearDown(self):
        super().tearDown()
        self.db_connection.close()
