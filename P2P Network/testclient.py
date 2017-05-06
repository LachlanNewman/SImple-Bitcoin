import socket

host = 'localhost' # '127.0.0.1' can also be used
port1 = 7001
port2 = 7002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connecting to socket
sock.connect((host, port1)) #Connect takes tuple of host and port
sock2.connect((host, port2)) #Connect takes tuple of host and port
#Infinite loop to keep client running.
while True:
    message = input('->')
    sock.send(message.encode())
    sock2.send(message.encode())

sock.close()
