from http import HTTPStatus

import uuid
import sqlite3
import tornado.web


class IdRegisterRequestHandler(tornado.web.RequestHandler):

    def initialize(self, db_connection):
        self.db_connection = db_connection

    async def post(self):
        user_id = str(uuid.uuid4())

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_ids WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()[0]

        if exists:
            self.post()
        else:
            cursor.execute("INSERT INTO user_ids (user_id) VALUES (?)", (user_id,))
            self.db_connection.commit()
            self.write({"success": f'User ID {user_id} registered successfully'})
