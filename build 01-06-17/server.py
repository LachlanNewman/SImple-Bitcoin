import socket, ssl, threading, json, time

connections = []

#Global so they can be edited across threads
global transmissionHistory
transmissionHistory = []
global completedMines
global actualTotalTime             #The observed time it takes to mine ^ many transactions
global target

#Lachlan Newman
#Initialises the server with user input
def initServer():
    #Get a port number from command line
    port = -1
    while(port == -1 or not port.isdigit()):
        port = input("Enter a valid, unregistered port number:\n")

    #Bind socket to port and host
    ssl_sock = socket.socket()
    ssl_sock.bind( ('', int(port)) ) 
    ssl_sock.listen(5)         #Listen to a que of connections
    
    #Return the socket
    return ssl_sock
   
#Isaac R. Ward
#Thread used to recalculate the network target appropriately
def targetRecalculator(targetTime, minesBeforeRecalculation, stop):
    #Begin with no mines, edit as a global variable, such that it is accessible across threads
    global completedMines
    completedMines = 0
    
    global actualTotalTime
    actualTotalTime = 0
    
    targetTotalTime = minesBeforeRecalculation * targetTime

    global target
    target = 8358781686668571119172666661644162112593021720622887683062055401684992         #This initial target should take only a few seconds to mine
    prevCompletedMines = 0

    #Checks against the ever increasing amount of completed mines and recalculates when necessary
    while not stop():
        #So that when 'completedMines % minesBeforeRecalculation == 0' a new target isn't calculated infinitely
        if ((completedMines == minesBeforeRecalculation)):
            #A new 'batch' of mines has been completed, target must be adjusted accordingly
            #If completed too quickly, ratio < 1, and target decreases making it harder to randomly
            #generate a number less than it
            #If completed too slowly, ratio > 1, and target increases making it easier to randomly
            #generate a number less than it
            ratio = actualTotalTime/targetTotalTime
            target = int(target*(ratio))
            
            print("The last " + str(minesBeforeRecalculation) + " mines required " + str(actualTotalTime) + "s when it should have taken " + str(targetTotalTime) + "s.")
            print("Difficulty out by ratio " + str(ratio) + ", yielding new target:\n" + str(target))
            
            #This is then transmitted to all nodes such that miners can update their local targets
            #Transmission is discarded in wallets and processed in miners
            transmission = {}
            transmission['header'] = "NEW TARGET"
            transmission['data'] = target
            for conn in connections:
                conn.send((json.dumps(transmission).encode()))

            actualTotalTime = 0       
            completedMines = 0   

#Lachlan Newman
#Isaac R. Ward
#Ran as a thread for each client, once in while loop the function acts as a receiver for transmissions
#on the given client's connection
def transmissionRecieved(clientStream, stop):
    print("Client logged in.")
    
    #A new client needs the network's history to ensure that they are up to date
    global transmissionHistory
    for t in transmissionHistory:
        clientStream.send(json.dumps(t).encode())
    
    #In the case that a miner has connected, immediately broadcast to the miner the network target
    #note that the target recalculator thread can also access the target, so this is a global variable
    targetInitMiner = {}
    targetInitMiner['header'] = "NEW TARGET"
    global target
    targetInitMiner['data'] = target
    clientStream.send(json.dumps(targetInitMiner).encode())
    
    #In the case that a wallet has connected, immediately broadcast to the wallet the network's
    #coinbase (mining reward), which will arbitrarily by 50 in our case here
    targetInitWallet = {}
    targetInitWallet['header'] = "NEW COINBASE"
    targetInitWallet['data'] = 50
    clientStream.send(json.dumps(targetInitWallet).encode())
    
    
    #Infinite loop so that function does not terminate and thread does not end, 
    #continuously 'listens' for client transmissions
    while not stop():
        #4096 stands for bytes of data to be received, decode this clients stream into a transmission if possible
        stream = clientStream.recv(4096).decode()
        if not stream:
            #Client has disconnected as empty socket transmission has been read, terminate thread
            connections.remove(clientStream)
            print("Client logged off.")
            break
        
        #Retransmit if data has been received
        transmission = json.loads(stream)   
        if transmission:
            #Save the transmission in transmission history in case a new client logs on
            transmissionHistory.append(transmission)
            
            #Sending to all connected clients
            print("Received transmission w/ header '" + transmission['header'] + "'; retransmitting to all clients.")
            
            for c in connections:
                c.send(json.dumps(transmission).encode())
                
            #Need to count completed mines to know when to recaculate network difficulty target
            if(transmission['header'] == "MINING COMPLETE"):
                #Ensure that we are editing the global server values such that they can be utilised in the target recalc thread
                global completedMines 
                completedMines = completedMines + 1
                
                global actualTotalTime
                actualTotalTime = actualTotalTime + ((transmission['data'])['metrics'])['t']

#Lachlan Newman
if __name__ == '__main__':
    #Call the socket code that initialises the server
    s = initServer()
    
    #Currently nobody on the network
    networkSize = 0
    
    #Seconds it should require to mine a transaction
    targetTime = int(input("How long in seconds should it take to mine one transaction on average:\n"))
    
    #How many completed mines required before the target is recalculated
    minesBeforeRecalculation = int(input("How many mines are required before the network target is recalculated? (a higher value will make it more likely to hit the specified target time):\n"))


    #Inital global network mining target recalculating thread
    stop = False
    targetThread = threading.Thread(target=targetRecalculator, args=(targetTime, minesBeforeRecalculation, lambda: stop))
    #Setting a thread to be a daemon ensures it will end when main does
    targetThread.daemon = True
    targetThread.start()
    
    #Ready for clients
    print("Waiting for clients to join.")
    
    while True:
        #Initialise servers socket
        newsocket, fromaddr = s.accept()
        
        #Ensure that all client who connect recieve ssl certificate
        connstream = ssl.wrap_socket(newsocket, server_side=True,
                                     certfile="mycert.pem",
                                     keyfile="mycert.pem")
        
        #Encode information of connection into a client dict and add to list

        connections.append(connstream)                #append the details of the connection to the connection list
        networkSize = networkSize + 1                   #number of users in the network increases by 1 for each connection
        
        #Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        clientThread = threading.Thread(target=transmissionRecieved,  
                                        args=(connstream, lambda: stop))
        #Setting a thread to be a daemon ensures it will end when main does
        clientThread.daemon = True
        clientThread.start()

    print("Ending server.")
    stop = True


