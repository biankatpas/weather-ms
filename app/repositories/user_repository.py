class UserRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_user_data_on_db(self, user_uuid):
        try:
            cursor = self.db_connection.cursor()

            cursor.execute("INSERT INTO user (id) VALUES (?)", (user_uuid,))
            self.db_connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()

        finally:
            cursor.close()

    def user_uuid_already_exists(self, user_uuid):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user WHERE id = ?", (user_uuid,))

        return cursor.fetchone()[0]
