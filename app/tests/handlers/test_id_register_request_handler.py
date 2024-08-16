import uuid
import pytest

import tornado.escape
import tornado.testing

from tornado.web import Application
from unittest.mock import MagicMock

from app.handlers.id_register_request_handler import IdRegisterRequestHandler
from app.services.request_service import RequestService
from app.fixtures.database_fixture import get_db_connection, initialize_db


@pytest.mark.asyncio
async def test_post_register_id():
    http_client = tornado.httpclient.AsyncHTTPClient()

    response = await http_client.fetch(
        "http://localhost:8888/user/register",
        method="POST",
        body=""
    )
    response_json = tornado.escape.json_decode(response.body)

    assert response.code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "user request id registered successfully"
    assert "user_request_id" in response_json["data"]
