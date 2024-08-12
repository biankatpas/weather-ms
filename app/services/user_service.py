from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.repository = UserRepository(self.db_connection)

    def process(self, user_uuid):
        if not self.repository.user_uuid_already_exists(user_uuid):
            self.repository.store_user_data_on_db(
                user_uuid=user_uuid
            )
            return True
        return False
