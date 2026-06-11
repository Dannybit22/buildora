from database.connection import DatabaseConnection


class QueryExecutor:
    @staticmethod
    def fetch_one(query, params=None):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result

        except Exception as error:
            print(f"Error en fetch_one: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def fetch_all(query, params=None):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result

        except Exception as error:
            print(f"Error en fetch_all: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def execute(query, params=None):
        connection = DatabaseConnection.get_connection()

        if not connection:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            return True

        except Exception as error:
            print(f"Error en execute: {error}")
            connection.rollback()
            return False

        finally:
            cursor.close()
            connection.close()