import uuid
import tornado.web

from http import HTTPStatus


class IdRegisterRequestHandler(tornado.web.RequestHandler):

    def initialize(self, db_connection):
        self.db_connection = db_connection

    async def post(self):
        user_uuid = str(uuid.uuid4())

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE id = ?", (user_uuid,))
        exists = cursor.fetchone()[0]

        # TODO: implement DB access code in user_repository.py
        if exists:
            self.post()
        else:
            cursor.execute("INSERT INTO user (id) VALUES (?)", (user_uuid,))
            self.db_connection.commit()
            response = {
                "status": "success",
                "message": "User ID registered successfully",
                "id": user_uuid
            }
            self.status_code = HTTPStatus.OK
            self.write(response)
