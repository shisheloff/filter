import os
import socket

ip_host = "0.0.0.0"
server_port = 514
BufferSize = 2048


sc = socket.socket()

sc.bind(ip_host, server_port)

sc.listen(5)

print(f"[INFO] Server listening as {ip_host}:{server_port}")

client_socket, address = sc.accept()

print(f"[+] {address} is connected.")

recivedFilename = client_socket.recv(BufferSize).decode()

recivedFilename = os.path.basename(recivedFilename)

with open(recivedFilename, 'wb') as f:
    while True:
        bytesRead = client_socket.recv(BufferSize)
        if not bytesRead:
            break
        f.write(bytesRead)
client_socket.close()
sc.close()



