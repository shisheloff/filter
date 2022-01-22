import os
import socket


def sendFiles():
    # filename = os.path.abspath("auth_logs.txt")
    filename = "auth_logs.txt"
    sk = socket.socket()
    # BufferSize = 4096
    ip_port = ('192.168.1.31', 514)

    sk.connect(ip_port)

    # sk.send(f"{filename}".encode())
    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read()
            if not bytesRead:
                break
            sk.sendall(bytesRead)
            print(f"[INFO] Sent {filename} on server")

    sk.close()


sendFiles()
