import socket
import sys
import threading
import ssl
import uuid
from subprocess import call
import pprint
import walletclass
import json

class Server(object):

    def __init__(self, host, port):
        self.host = host #host name
        self.port = port #port for server
        self.id   = uuid.uuid4()
        self.wallet = walletclass.Wallet()

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
            print("data\n")
            print(data['id'])
            #users['id'] = data[1]
            #print("users\n\n")
            #print(users) #TODO add public and port to users - keys
            #print("endkssognsin\n")
            self.wallet.intial_transactions(data['id'])

        self.connection, self.address = self.socket.accept()
        print("connnecetion")
        while True:
            data = self.connection.recv(1024).decode()
            if not data:
                break;
            print("from user " + str(data))
            if '-----BEGIN PUBLIC KEY-----' in str(data):
                addToUsers(json.loads(data))
            else:
                print("from thread:" , threading.current_thread(), data)

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
