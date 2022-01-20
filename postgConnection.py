import psycopg2
from config import host, user, password, db_name
def psqlConnect():
    try:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"Server version: {cursor.fetchone()}")

    except Exception as _ex:
        print("[INFO] Error while working with postgresql database", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] postgresql connection closed")

