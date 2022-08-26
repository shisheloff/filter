import psycopg2
from config.config import host, user, password, db_name

try:
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)

    with connection.cursor() as cursor:
        cursor.execute("drop table datastore")
        connection.commit()
        print(f"Database dropped {cursor.fetchone()}")

except Exception as _ex:
    print("[ERROR]: ", _ex)
finally:
    if connection:
        connection.close()
