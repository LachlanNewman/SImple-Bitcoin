import socket, ssl, threading, json, time
#Get a port number from command line
port = -1
socket = socket.socket()
while(port == -1 or not port.isdigit()):
    port = input("Enter a valid, unregistered port number:\n")

    #bind socket to port and host

while(socket.bind( ('', int(port)) ) == -1):
        port = input("Error binding socket to port, please try another port number:")

socket.listen(5)         #listen to a que of connections
num_clients = 2          #TODO amke num of user input from command line
clientConnections = []   #list of connection detials for each client to server
clientPublicKeys  = []   #list of the publickeys for each client
networkSize       = 0    #initailse the number of users in the network
target            = 2**256
target_count      = 0
target_change     = 50
#TODO RECIEVE BLOCK functions
#TODO reclaibrate target and send to client
#TODO send signal to all other users to stop mining when sig is received from winning
#TODO sever has to be able send new blocks new taget stop mining and transactions to all clients

def mined(mine):
    target_count = target_count + 1
    if target_count % target_change == 0
        #reclaibrate_target
    for conn in clientConnections:
        conn.send((json.dumps(mine).encode()))
    #send new target to all other clients

def transactionRecieved(transaction):
    for conn in clientConnections:
        conn.send((json.dumps(transaction).encode()))


#------------------------------------------------------------------------------------------------------------------------------------------
#Send the public keys of the users in the netwrok to every user
#------------------------------------------------------------------------------------------------------------------------------------------
def sendPublicKeys(clientConnections):
    #print("sending public keys")
    for conn in clientConnections:                  #for each socket connection between a client
        for client in clientPublicKeys:             #send each clients public key
            conn.send((json.dumps(client).encode()))
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------
#runs in a seperate thread to enable mutiple clients to connecto to the server
#------------------------------------------------------------------------------------------------------------------------------------------
def clientthread(connstream,networkSize):
    #infinite loop so that function do not terminate and thread do not end.
    print(networkSize)
    while True:
        data = connstream.recv(4096).decode()       # 1024 stands for bytes of data to be received
        if not data:
            break
        data = json.loads(data)
        if data['header'] == "publickey":
            clientPublicKeys.append(data)   #append the public key to the list of public keys TODO condition to check if pubic keys or transaction
        elif data['header'] == "transaction":
            transactionRecieved(data)
        elif data['header'] == "mined":
            mined()
        else:
            print("not a recognised heaeder message ignored")

if __name__ == '__main__':

    while True:
        newsocket, fromaddr = socket.accept() #initialise servers socket
        #ensure that all client who connect recieve ssl certificate
        connstream = ssl.wrap_socket(newsocket, server_side=True,
                                     certfile="mycert.pem",
                                     keyfile="mycert.pem")

        networkSize = networkSize + 1                   #number of users in the network increases by ! for each connection
        clientConnections.append(connstream)            #append the details of the connection to the connection list
        client = threading.Thread(target=clientthread,  #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
                        args=(connstream,networkSize))
        client.start()                                  #start thread for client

        if(networkSize == num_clients):                 #if the network size reaches maximum TODO make input for runtime of maximum network size
            time.sleep(3)                               #ensures final public key is added to publickeys list
            sendPublicKeys(clientConnections)           #send the public keys to all clients
