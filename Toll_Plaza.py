import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_to_database():
    """Establishes a connection to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                      password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def close_connection(connection):
    """Safely closes the database connection."""
    if connection:
        try:
            connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")


class TollPlaza:
    """Represents a TollPlaza object for interacting with toll plaza data."""

    def __init__(self, connection):
        self.connection = connection

    def get_all_toll_plazas(self):
        """Retrieves all toll plaza data from the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("select * from toll_plaza")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error getting all toll plazas: {e}")
            return None
        finally:
            cursor.close()

    def get_toll_plaza_by_id(self, id):
        """Retrieves toll plaza data for a specific ID."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "select * from toll_plaza tp, toll t where t.toll_id=tp.toll_plaza_id and tp.toll_plaza_id=%s", (id,))
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error getting toll plaza by ID: {e}")
            return None
        finally:
            cursor.close()


connection = connect_to_database()
if connection:
    toll_plaza_obj = TollPlaza(connection)
    all_toll_plazas = toll_plaza_obj.get_all_toll_plazas()
    specific_toll_plaza = toll_plaza_obj.get_toll_plaza_by_id(
        1)  # Replace 1 with the desired ID

    if all_toll_plazas:
        print("All Toll Plazas:")
        for row in all_toll_plazas:
            print(row)  # Access data from each row

    if specific_toll_plaza:
        print("Toll Plaza with ID 1:")
        for row in specific_toll_plaza:
            print(row)

    close_connection(connection)
else:
    print("Error connecting to database")
