import psycopg2
from config.config import host, user, password, db_name
import bin.syslog


def psqlConnect():
    try:
        connection = psycopg2.connect(host=host,
                                      user=user,
                                      password=password,
                                      database=db_name
                                      )

        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"Server version: {cursor.fetchone()}")

    except Exception as _ex:
        print("[INFO] Error while working with postgresql database", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] postgresql connection closed")


try:
    with open("auth_logs.txt", "r") as file:
        connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS datastore ("
                           "Month  text,"
                           "Day int,"
                           "Time text,"
                           "Domain text,"
                           "Sender text,"
                           "Message text"
                           ");")
            # connection.commit()
            print("[INFO] Table created!")
            while True:
                line = file.readline()
                data = bin.syslog.parser(line)
                for key, value in data.items():
                    print("INSERT INTO datastore (%s) VALUES (%s)" % key % value)
                    cursor.execute("INSERT INTO datastore ({0}) VALUES ({1})".format(key, str(value)))
            connection.commit()
            connection.close()
except Exception as _ex:
    print("[Err]: Error connecting to database.", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] postgresql connection closed")

'''
with open("auth_logs.txt", "r") as f:
    line = f.readline()
    # print(line)
    data = bin.syslog.parser(line)
    print(data.values())
                    for i in values:
                    cursor.execute("INSERT INTO public.datastore (Month, Day, Time, Domain, Sender, Message) "
                                   "VALUES ({})".format(i))
'''
