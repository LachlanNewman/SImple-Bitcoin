
import serverclass
import clientclass
import multiprocessing
import time
import sys
import os

HOST = 'localhost'
PORT = 8000

#COMMANDS
GETUSERS = "RUN GETUSERS" #Connects user to peers in network
ENDCONN  = "RUN ENDCONNECTION" #Ends connection with user to peers


#Server and Client are run on different processes, this allows to server
#to accept infomation from multiple other clients but also allow to send to
#other users without processing the data through a third party
#--------------------------------------------------------------------------


#Client process
#-------------------------------------------------------------------------------
def clientAction(q,fileno):
    sys.stdin = os.fdopen(fileno)    #open stdin in this process
    client    = clientclass.Client() #create empty Client

    client.createUser()              #get userid and port client in running on
    client.getPortsUsed()            #get ports peers are running on TODO all servers post ports to online database

    if(input('Enter "RUN GETUSERS to connect to peers":')==GETUSERS): #command to get all users
        if(client.connectClient()):
            message ="CLIENT:" + str(client.user['id']) + "has connect to peers\n"
            while message!= ENDCONN:        #message in not to end the connection
                client.sendMessage(message) #send message to all peers TODO only send privatemeesage to specific port
                message = input('Send Message or Enter "RUN ENDCONNECTION to disconnect to peers":')
        else:
            print("connection failed")

    client.closeSockets() # close all sockets client is connected to
#-------------------------------------------------------------------------------


#Server Process
#-------------------------------------------------------------------------------
def serverAction():
    server = serverclass.Server(HOST,PORT) #create Server running on loalhost and port TODO maker server run over internet
    server.connectServer()                 #connect the Server
    print("port in use = ", server.port)
    #TODO upload port used with client
    server.connectClient()                 #create a socket connection in server
    server.acceptClients()                 #server begins to accept users to connect
#-------------------------------------------------------------------------------

q = multiprocessing.Queue()
fn = sys.stdin.fileno()                                             #get original file descriptor for stdin
client = multiprocessing.Process(target=clientAction,args=(q,fn))   #client process
server = multiprocessing.Process(target=serverAction)               #server process
server.start()                                                      #start server process
time.sleep(2)                                                       #timer used to make sure output in correct
client.start()                                                      #start client process
client.join()
server.join()
