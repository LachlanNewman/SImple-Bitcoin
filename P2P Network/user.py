
import serverclass
import clientclass
import multiprocessing
import time
import sys
import os
import cryptographyfunctions
import walletclass

HOST = '127.0.0.1'
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
def clientAction(user,users,fileno):
    crypto = cryptographyfunctions.Crypto()
    sys.stdin = os.fdopen(fileno)    #open stdin in this process
    client    = clientclass.Client() #create empty Client

    client.createUser(user)
    client.getPortsUsed()            #get ports peers are running on TODO all servers post ports to online database

    if(input('Enter "RUN GETUSERS to connect to peers":')==GETUSERS): #command to get all users
        if(client.connectClient()):
            message ="CLIENT:" + str(client.user['id']) + "has connect to peers\n"
            client.sendSLL()
            while message!= ENDCONN:
                print("users\n\n")
                print(users)
                print("end\n\n")
                reciever = input("send bit coins to: ")
                #TODO search wallet to make sure user has amout
                client.sendMessage(message) #send message to all peers TODO only send privatemeesage to specific port
                message = crypto.buildTransactionDict(user['id'], "reciever", "transaction")
        else:
            print("connection failed")

    client.closeSockets() # close all sockets client is connected to
#-------------------------------------------------------------------------------


#Server Process
#-------------------------------------------------------------------------------
def serverAction(user,users):
    wallet = walletclass.Wallet()
    server = serverclass.Server(HOST,PORT) #create Server running on loalhost and port TODO maker server run over internet
    server.connectServer()                 #connect the Server
    print("port in use = ", server.port)
    #TODO upload port used with client
    server.getUser(user)
    server.genRSAKeyPairs(user)
    server.acceptClients(user)
                     #server begins to accept users to connect

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    user = multiprocessing.Manager().dict()
    users = multiprocessing.Manager().dict()
    fn = sys.stdin.fileno()                                             #get original file descriptor for stdin
    client = multiprocessing.Process(target=clientAction,args=(user,users,fn))   #client process
    server = multiprocessing.Process(target=serverAction, args=(user,users))               #server process
    server.start()
    #print(user['user'])                                                      #start server process
    time.sleep(2)                                                       #timer used to make sure output in correct
    client.start()                                                      #start client process
    client.join()
    server.join()
