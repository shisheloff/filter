import os
import socket
import psycopg2
import bin.syslog
from config.config import host, user, password, db_name
print(os.path.abspath("auth_logs.txt"))
ip_host = "0.0.0.0"
server_port = 514
# BufferSize = 10000
recivedFilename = "logs/syslog.txt"

def reciveFile():
    sc = socket.socket()

    sc.bind((ip_host, server_port))

    sc.listen(10)

    print(f"[INFO] Server listening as {ip_host}:{server_port}")

    client_socket, address = sc.accept()

    print(f"[+] {address} is connected.")

    # recivedFilename = client_socket.recv(BufferSize).decode()

    # recivedFilename = os.path.basename(recivedFilename)
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


'''
    with open(recivedFilename, "r") as f:
        data = f.readlines()
        for lines in data:
            print(bin.syslog.parser(lines))
'''

def insertData(fileWithData):
    with open(recivedFilename, "r") as file:
        try:
            connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
            with connection.cursor() as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS datastore ("
                               "Month VARCHAR(10),"
                               "Day VARCHAR(10),"
                               "Time VARCHAR(10),"
                               "Domain VARCHAR(25),"
                               "Sender VARCHAR(10),"
                               "Message VARCHAR(100)"
                               ");")
                connection.commit()
                while True:
                    line = file.readline()
                    data = bin.syslog.parser(line)
                    cursor.execute("INSERT INTO datastore (Month, Day, Time, Domain, Sender, Message) "
                                   "VALUES (%s, %s, %s, %s, %s, %s)", data.get('month'),
                                   data.get('day'), data.get('time'), data.get('domain'),
                                   data.get('sender'), data.get('message'))
        except Exception as _ex:
            print("[Err]: Error connecting to database.", _ex)
        finally:
            if connection:
                connection.close()


reciveFile()

