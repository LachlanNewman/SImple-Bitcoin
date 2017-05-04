
import serverclass
import clientclass
import multiprocessing
import time


def clientAction():

    print("client port in use")

def serverAction():
    server = serverclass.Server('localhost',8000)
    port = server.port
    print("port in use = ", port)
    server.connectServer()
    print("socket connected")
    server.connectClient()
    server.acceptClients()


client = multiprocessing.Process(target=clientAction)
server = multiprocessing.Process(target=serverAction)
server.start()
client.start()
client.join()
server.join()
