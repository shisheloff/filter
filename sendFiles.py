import os
import socket
def sendFiles():
    filenames = ["linux.txt", "windows.txt"]
    sk = socket.socket()
    BufferSize = 2048
    ip_port = ('127.0.0.1', 514)

    sk.connect(ip_port)
    for name in filenames:
        sk.send(f"{name}".encode())
        with open(f"{name}", "rb") as f:
            while True:
                bytesRead = f.read(BufferSize)
                if not bytesRead:
                    break
                sk.sendall(bytesRead)
                print(f"[INFO] Sent {name} on server")

    sk.close()
