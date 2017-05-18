import socket
import sys
import threading
import ssl
import uuid
from subprocess import call
import pprint
class Server(object):

    def __init__(self, host, port):
        self.host = host #host name
        self.port = port #port for server
        self.id   = uuid.uuid4()

    def connectServer(self):
        self.socket = socket.socket()
        while True:#while loop keeps socket open until client disconects
            try:
                #test to see if the port is open
                self.socket.bind((self.host,self.port))
                break
            except socket.error as e:
                if e.errno == 98:
                    print("Port is already in use")
                    self.port += 1#add 1 to try another port and see if it is open
                else:
                    print(e)
        self.socket.listen(5)

    def acceptClients(self,users):
        pp = pprint.PrettyPrinter(indent=4)

        def addToUsers(data):
            data = data.split(":")
            users[data[0]] = data[1]
            pp.pprint(users)

        def clientthread(connstream):
            #infinite loop so that function do not terminate and thread do not end.
             while True:
                data = connstream.read()# 1024 stands for bytes of data to be received
                if not data:
                    continue
                else:
                    if '-----BEGIN PUBLIC KEY-----' in str(data):
                        addToUsers(data.decode())
                    else:
                        print("from thread:" , threading.current_thread(), data)
        #allow socket to accept connection from clients

        for i in range(5):

            self.connection, self.address = self.socket.accept()
            print("connnecetion")

            try:
                connstream = ssl.wrap_socket(self.connection,
                                                server_side=True,
                                                 certfile="mycert.pem",
                                                 keyfile="mycert.pem")
            except socket.error as e:
                print("SERVERError[" + str(e.errno) + "]: " + e.strerror)
                break

            #Creating new thread. Calling clientthread function for this function and passing conn as argument.
            client = threading.Thread(target=clientthread,args=(connstream,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client.start()

        self.connection.close()
        self.socket.close

    def genRSAKeyPairs(self,user):
        #Use OpenSSL to generate given bit modulus RSA keys NOT using Triple Data Encryption (-des3)
        call(["openssl", "genrsa", "-out", "private" + user['id'] + ".pem", "2048"])

        #Write public key out to new file named publicX.pem
        call(["openssl", "rsa", "-in", "private" + user['id'] + ".pem", "-outform", "PEM", "-pubout", "-out", "public" + user['id'] + ".pem"])

    def getUser(self,user):

        user['port'] = str(self.port)
        user['id']   = str(self.id)
        print("client action")
