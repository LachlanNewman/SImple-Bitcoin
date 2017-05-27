import socket, ssl, threading, json, time

global connections
connections = []

global completedMines
global actualTotalTime             #The observed time it takes to mine ^ many transactions

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
    
#Thread used to recalculate the network target appropriately
def targetRecalculator():
    #Begin with no mines, completed mines is edited as a global variable, such that it is accessible across threads
    global completedMines
    completedMines = 0
    
    global actualTotalTime
    actualTotalTime = 0
    
    minesBeforeRecalculation = 3    #How many completed mines required before the target is recalculated
    targetTime = 120                #Seconds it should require to mine a transaction
    targetTotalTime = minesBeforeRecalculation * targetTime

    target = 2**256                 #Easiest possible initial target
    prevCompletedMines = 0

    #Checks against the ever increasing amount of completed mines and recalculates when necessary
    while(True):
        #So that when 'completedMines % minesBeforeRecalculation == 0' a new target isn't calculated infinitely
        if ((completedMines % minesBeforeRecalculation == 0.0) and (completedMines != prevCompletedMines)):
            #A new 'batch' of mines has been completed, target must be adjusted accordingly
            #If completed too quickly, ratio < 1, and target decreases making it harder to randomly
            #generate a number less than it
            #If completed too slowly, ratio > 1, and target increases making it easier to randomly
            #generate a number less than it
            ratio = actualTotalTime/targetTotalTime
            target = int(target*(ratio))
            
            print("Difficulty out by ratio " + str(ratio) + ", yielding new target:\n" + str(target))
            
            #This is then transmitted to all nodes such that miners can update their local targets
            #Transmission is discarded in wallets and processed in miners
            transmission = {}
            transmission['header'] = "NEW TARGET"
            transmission['data'] = target
            for conn in connections:
                conn.send((json.dumps(transmission).encode()))

            actualTotalTime = 0       
            prevCompletedMines = completedMines    
    
#Ran as a thread for each client, once in while loop the function acts as a receiver for transmissions
#on the given client's connection
def transmissionRecieved(clientStream):
    print("Client logged in.")
    
    #Infinite loop so that function does not terminate and thread does not end, 
    #continuously 'listens' for client transmissions
    while True:
        #Only accepted headers FROM client TO server are:
            #TRANSACTION
            
        #Only accepted headers FROM miner TO server are:
            #MINE SIGNAL
        
        #4096 stands for bytes of data to be received, decode this clients stream into a transmission
        transmission = json.loads(clientStream.recv(4096).decode())   
        
        #Retransmit if data has been received
        if transmission:    
            print("Received transmission w/ header '" + transmission['header'] + "'; retransmitting to all clients.")
            
            #Need to count completed mines to know when to recaculate network difficulty target
            if(transmission['header'] == "MINING COMPLETE"):
                global completedMines 
                completedMines = completedMines + 1
                
                global actualTotalTime
                actualTotalTime = actualTotalTime + ((transmission['data'])['metrics'])['t']
            
            for c in connections:
                c.send(json.dumps(transmission).encode())


            
if __name__ == '__main__':
    #Call the socket code that initialises the server
    s = initServer()
    
    #Currently nobody on the network
    networkSize = 0
    
    #Inital global network mining target recalculating thread
    targetThread = threading.Thread(target=targetRecalculator, args=())
    targetThread.start()
    
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
                        args=(connstream,))               
        clientThread.start()        
                             

