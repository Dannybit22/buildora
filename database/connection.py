import mysql.connector
from mysql.connector import Error
from config.database_config import DB_CONFIG


class DatabaseConnection:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)

            if connection.is_connected():
                return connection

            return None

        except Error as error:
            print(f"Error de conexión a MySQL: {error}")
            return None

    @staticmethod
    def test_connection():
        connection = DatabaseConnection.get_connection()

        if connection:
            connection.close()
            return True

        return False