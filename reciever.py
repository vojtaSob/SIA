import hashlib
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
file_hash_calculated = hashlib.sha256()

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
mystring = data.decode('UTF-8')
if mystring.startswith("NAME="):
    strList = mystring.split("=")
    fileName = strList[1]
    strList.clear()
    data, addr = sock.recvfrom(1024)
    mystring = data.decode('UTF-8')
    strList = mystring.split("=")
    fileSize = strList[1]
    WRITE_TO_FILE = False
    data, addr = sock.recvfrom(1024)
    mystring = data.decode('UTF-8')
    if mystring.startswith("START"):
        print("Start of file transfer!")
        WRITE_TO_FILE = True
        with open(fileName, "wb") as f:
            while WRITE_TO_FILE:
                data, addr = sock.recvfrom(1024)
                try:
                    str = data.decode("UTF-8")
                    if str.startswith("END"):
                        print("END of file reached")
                        break
                except ValueError:
                    print("Image data accepted")
                file_hash_calculated.update(data)
                f.write(data)

    data, addr = sock.recvfrom(1024)
    str = data.decode("UTF-8")
    if str.startswith("HASH="):
        strList = str.split("=")
        file_hash_recieved = strList[1]
        if file_hash_recieved == file_hash_calculated.hexdigest():
            print("Hash is correct")
            print("File was transferred successfully!")


