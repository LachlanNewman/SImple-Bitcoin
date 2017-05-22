import socket
import sys
import ssl
import uuid
import json

class Client(object):

    def createUser(self,user):
        self.user = {}
        self.user['id'] = user['id']
        print(self.user)

    def connectClient(self):
        self.sockets = {}
        self.sslsockets={}
        for port in self.ports:
            self.sockets['socket_'+ port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.sockets['socket_'+ port].connect(('localhost',int(port)))
            except socket.error as e:
                print("CLIENTError[" + str(e.errno) + "]: " + e.strerror)
                return False
        return True

    def sendSLL(self):
        public = ""
        public_file = open("public"+self.user['id']+".pem", 'r')
        for line in public_file:
            public = public + line
        public_file.close()
        self.user['publickey'] = public
        user = json.dumps(self.user)
        for port in self.ports:
            self.sockets['socket_' + port].send(user.encode())


    def sendMessage(self,message):
        json_message = json.dumps(message)
        for port in self.ports:
            self.sockets['socket_' + port].send(json_message.encode())

    def getPortsUsed(self):
        csp = open('csp.txt', 'r')
        self.ports = csp.read().splitlines()
        csp.close()

    def closeSockets(self):
        for port in self.ports:
            self.sockets['socket_'+ port].close()
