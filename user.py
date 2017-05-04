
import serverclass
import threading
import time


def clientAction():
    global port
    shared.acquire()
    print("client port in use", port)

def serverAction():
    global port
    shared.acquire()
    server = serverclass.Server('localhost',8000)
    port = server.port
    print("port in use = ", port)
    #server.connectServer()
    #print("socket connected")
    #server.connectClient()
    #server.acceptClients()

shared = threading.Condition()
client = threading.Thread(target=clientAction)
server = threading.Thread(target=serverAction)
server.start()
time.sleep(1)
client.start()
client.join()
server.join()
