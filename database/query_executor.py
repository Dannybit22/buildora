from database.connection import DatabaseConnection


class QueryExecutor:
    @staticmethod
    def fetch_one(query, params=None):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Exception as error:
            print(f"Error en fetch_one: {error}")
            return None
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @staticmethod
    def fetch_all(query, params=None):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return []

        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Exception as error:
            print(f"Error en fetch_all: {error}")
            return []
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @staticmethod
    def execute(query, params=None):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return False

        cursor = None
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
            if cursor:
                cursor.close()
            connection.close()

    @staticmethod
    def execute_return_id(query, params=None):
        connection = DatabaseConnection.get_connection()
        if not connection:
            return None

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.lastrowid
        except Exception as error:
            print(f"Error en execute_return_id: {error}")
            connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            connection.close()