import uuid
import tornado.web

from http import HTTPStatus

from app.services.user_service import RequestService


class IdRegisterRequestHandler(tornado.web.RequestHandler):

    def initialize(self, db_connection):
        self.db_connection = db_connection

        self.service = RequestService(self.db_connection)

    async def post(self):
        user_uuid = str(uuid.uuid4())

        if not self.service.process(user_uuid):
            self.post()

        response = {
            "status": "success",
            "message": "user request id registered successfully",
            "data": {"user_request_id": user_uuid}
        }

        self.status_code = HTTPStatus.OK

        self.write(response)
