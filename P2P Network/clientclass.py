import socket
import sys
import ssl
import uuid

class Client(object):

    def createUser(self,user):
        self.user = user

    def connectClient(self):
        self.sockets = {}
        self.sslsockets={}
        for port in self.ports:
            self.sockets['socket_'+ port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.sslsockets['ssl_socket'+ port] = ssl.wrap_socket(self.sockets['socket_'+ port], ca_certs="mycert.pem", cert_reqs=ssl.CERT_REQUIRED)
                self.sslsockets['ssl_socket'+ port].connect(('localhost',int(port)))
            except socket.error as e:
                print("CLIENTError[" + str(e.errno) + "]: " + e.strerror)
                return False
        return True
    def sendSLL(self):
        public = ""
        public_file = open("public"+self.user['id']+".pem", 'r')
        for line in public_file:
            #Drop headers
            #if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            public = public + line
        public_file.close()

        #print(public)
        for port in self.ports:
            self.sslsockets['ssl_socket' + port].write((self.user['id'] +":" +public).encode())


    def sendMessage(self,message):
        for port in self.ports:
            self.sslsockets['ssl_socket' + port].write((self.user['id'] + ":" +message).encode())

    def getPortsUsed(self):
        csp = open('csp.txt', 'r')
        self.ports = csp.read().splitlines()
        csp.close()

    def closeSockets(self):
        for port in self.ports:
            self.sockets['socket_'+ port].close()
