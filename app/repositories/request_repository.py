import sqlite3

class RequestRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_request_data_on_db(self, user_uuid):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO request (id) VALUES (?)", (user_uuid,))
            self.db_connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e} - user_uuid might already exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()

    def store_request_total_items_to_process(self, user_uuid, totals):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("UPDATE request SET total = ? WHERE id = ?", (totals, user_uuid))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO request (id, total) VALUES (?, ?)", (user_uuid, totals))
            self.db_connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e} - user_uuid might already exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()

    def request_uuid_exists(self, user_uuid):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM request WHERE id = ?", (user_uuid,))
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            cursor.close()

    def get_request_total_items_to_process(self, user_uuid):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT total FROM request WHERE id = ?", (user_uuid,))
            result = cursor.fetchone()
            if result is None or result[0] is None:
                return 0
            return result[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
