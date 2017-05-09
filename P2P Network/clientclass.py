import socket
import sys
import ssl

class Client(object):

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

    def sendMessage(self,message):
        for port in self.ports:
            self.sslsockets['ssl_socket' + port].write(message.encode())

    def getPortsUsed(self):
        csp = open('csp.txt', 'r')
        self.ports = csp.read().splitlines()
        csp.close()
