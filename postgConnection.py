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
                           "Month TEXT,"
                           "Day TEXT,"
                           "Time TEXT,"
                           "Domain TEXT,"
                           "Sender TEXT,"
                           "Message TEXT"
                           ");")
            print("[INFO] Table created!")
            while True:
                line = file.readline()
                if not line:
                    break
                data = bin.syslog.parser(line)
                records = ", ".join(["%s"] * len(data.values()))
                cursor.execute(f"INSERT INTO datastore (month, day, time, domain, sender,"
                               f"message) VALUES ({records})", list(data.values()))
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
                    tup = [(k, v) for k, v in data.items()]
                print(tup)
                records = ", ".join(["%s"] * len(tup))
                cursor.execute(f"INSERT INTO datastore (month, day, time, domain, sender,"
                               f"message) VALUES ({records})", tup)
'''
