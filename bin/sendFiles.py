import socket


def sendFiles():
    filename = "/Users/21shish/PycharmProjects/lsfilter/auth_logs.txt"
    sk = socket.socket()

    ip_port = ('localhost', 514)

    sk.connect(ip_port)

    with open(filename, "rb") as f:
        while True:
            bytesRead = f.read()
            if not bytesRead:
                break
            sk.sendall(bytesRead)
            print(f"[INFO] Sent {filename} on server")

    sk.close()


sendFiles()
