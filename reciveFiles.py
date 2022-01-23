import socket
import psycopg2
import bin.syslog
from config.config import host, user, password, db_name
ip_host = "0.0.0.0"
server_port = 514
recivedFilename = "logs/syslog.txt"

def reciveFile():
    sc = socket.socket()

    sc.bind((ip_host, server_port))

    sc.listen(10)

    print(f"[INFO] Server listening as {ip_host}:{server_port}")

    client_socket, address = sc.accept()

    print(f"[+] {address} is connected.")

    with open(recivedFilename, 'wb') as f:
        print(f"[INFO] reciving file: {recivedFilename} ")
        while True:
            bytesRead = client_socket.recv(4096)
            if not bytesRead:
                break
            f.write(bytesRead)
        print(f"[INFO] recieved file {recivedFilename} successfully!")
    client_socket.close()
    sc.close()


def insertData(recivedFilename):
    with open(recivedFilename, "r") as file:
        try:
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

        except Exception as _ex:
            print("[Err]: Error --->", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] postgresql connection closed")


reciveFile()
insertData(recivedFilename)
