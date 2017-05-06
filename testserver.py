import socket
#Importing all from thread
import threading

# Defining server address and port
host = ''  #'localhost' or '127.0.0.1' or '' are all same
#port = 7001 #Use port > 1024, below it all are reserved
port = 7002

#Creating socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(5) #5 denotes the number of clients can queue

def clientthread(conn):
#infinite loop so that function do not terminate and thread do not end.
     while True:
        data = conn.recv(1024).decode() # 1024 stands for bytes of data to be received
        if not data:
            continue
        else:
            print("from thread:" , threading.current_thread(), data)
        #allow socket to accept connection from clients

while True:
    connection, address = sock.accept()
    #Creating new thread. Calling clientthread function for this function and passing conn as argument.
    client = threading.Thread(target=clientthread,args=(connection,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    client.start()

connection.close()
socket.close
