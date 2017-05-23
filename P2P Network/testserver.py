import socket, ssl, threading, json, time

if __name__ == '__main__':

    socket = socket.socket() #create socket
    socket.bind(('', 10000)) #bind socket to port and host TODO make over network and check if port is open
    socket.listen(5)         #listen to a que of connections
    num_clients = 2          #TODO amke num of user input from command line
    clientConnections = []   #list of connection detials for each client to server
    clientPublicKeys  = []   #list of the publickeys for each client
    networkSize       = 0    #initailse the number of users in the network

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
            data = connstream.read().decode()   # 1024 stands for bytes of data to be received
            if not data:
                break
            try:
                data = json.loads(data)
                clientPublicKeys.append(data)   #append the public key to the list of public keys TODO condition to check if pubic keys or transaction
            except:
                #print(data)
        connstream.close()  #close the socket connection
    #------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------



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
