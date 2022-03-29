import os
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Karel"

file_name = "input.jpg"

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.sendto(bytes("NAME=" + file_name, "utf-8"), (UDP_IP, UDP_PORT))
file_size = os.path.getsize(file_name)
sock.sendto(bytes("SIZE=" + str(file_size), "utf-8"), (UDP_IP, UDP_PORT))
sock.sendto(bytes("START", "utf-8"), (UDP_IP, UDP_PORT))

current_size = 0
with open(file_name, 'rb') as f:
    while current_size < file_size:
        sock.sendto(f.read(1024), (UDP_IP, UDP_PORT))
        current_size += 1024

sock.sendto(bytes("END", "utf-8"), (UDP_IP, UDP_PORT))

sock.close()
