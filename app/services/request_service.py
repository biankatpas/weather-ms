from app.repositories.request_repository import RequestRepository


class RequestService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.repository = RequestRepository(self.db_connection)

    # TODO: rename it
    def process(self, user_uuid):
        self.repository.store_request_data_on_db(
            user_uuid=user_uuid
        )

    def request_uuid_exists(self, user_uuid):
        return self.repository.request_uuid_exists(user_uuid)
