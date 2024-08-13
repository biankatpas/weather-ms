from app.repositories.request_repository import RequestRepository


class RequestService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.repository = RequestRepository(self.db_connection)

    def store_request_uuid(self, uuid):
        self.repository.store_request_uuid_to_process(
            uuid=uuid
        )

    def store_total_items(self, uuid, totals):
        self.repository.store_request_total_items_to_process(
            uuid=uuid,
            totals=totals
        )

    def request_uuid_exists(self, uuid):
        return self.repository.request_uuid_exists(uuid)
