import sqlite3

class RequestRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def store_request_uuid_to_process(self, uuid):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("INSERT INTO request (id) VALUES (?)", (uuid,))
            self.db_connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e} - uuid might already exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()

    def store_request_total_items_to_process(self, uuid, totals):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("UPDATE request SET total = ? WHERE id = ?", (totals, uuid))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO request (id, total) VALUES (?, ?)", (uuid, totals))
            self.db_connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e} - uuid  might already exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.db_connection.rollback()
        finally:
            cursor.close()

    def request_uuid_exists(self, uuid):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM request WHERE id = ?", (uuid,))
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            cursor.close()

    def get_request_total_items_to_process(self, uuid):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT total FROM request WHERE id = ?", (uuid,))
            result = cursor.fetchone()
            if result is None or result[0] is None:
                return 0
            return result[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cursor.close()
