import psycopg2

import sendFiles
import postgConnection
import reciveFiles
from config.config import host, user, password, db_name

try:
    connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS Database ("
                       "Month VARCHAR(10),"
                       "Day VARCHAR(10),"
                       "Time VARCHAR(10),"
                       "Domain VARCHAR(25),"
                       "Sender VARCHAR(10),"
                       "Message VARCHAR(100)"
                       ");")
except Exception as _ex:
    print("[Err]: Error connecting to database.")
finally:
    if connection:
        connection.close()

reciveFiles.reciveFile()





