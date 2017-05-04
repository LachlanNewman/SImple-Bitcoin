
import serverclass
import clientclass
import multiprocessing
import time
import sys
import os


def clientAction(q,fileno):
    sys.stdin = os.fdopen(fileno)  #open stdin in this process
    client    = clientclass.Client()
    print("client port in use")
    client.connectClient()
    message = input('->')
    while message!='ENDCONN':
        client.sendMessage(message)
        message = input('->')

def serverAction():
    server = serverclass.Server('localhost',8000)
    server.connectServer()
    port   = server.port
    print("port in use = ", port)
    print("socket connected")
    server.connectClient()
    server.acceptClients()

q = multiprocessing.Queue()
fn = sys.stdin.fileno() #get original file descriptor for stdin
client = multiprocessing.Process(target=clientAction,args=(q,fn))
server = multiprocessing.Process(target=serverAction)
server.start()
client.start()
client.join()
server.join()
