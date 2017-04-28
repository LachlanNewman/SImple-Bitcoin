import socket
import sys


HOST = 'localhost'   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST,PORT))
print("Client connected to socket")

test = [1,19, "eleven"]

message = input("->")

while message != 'ENDCONN':
    clientSocket.send(message.encode())
    clientSocket.send(test.encode())
    message= clientSocket.recv(1024).decode()
    print(message)
    message = input('->')

clientSocket.close()
