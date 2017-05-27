import socket, ssl, pprint, uuid, subprocess, json, threading, sys, os.path
from crypto3002 import *

global gMiningComplete 
gMiningComplete = []

#Easiest possible initial target, will mine in one attempt
global target
target = 2**256

def createSSLSocket():
    #Generate a stream style socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Require a certificate from the server. We used a self-signed certificate
    #so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,
                               ca_certs="mycert.pem",
                               cert_reqs=ssl.CERT_REQUIRED)
    
    #Get port number of server as user input and connect
    port = input("Enter server's port number:\n")
    ssl_sock.connect(('localhost', int(port)))
    
    return ssl_sock

#Receives any data from the server
def receive(ssl_sock):
    #Will be ran as a continuously looping thread that waits for received transmissions
    while(True):            
        #Load transmission
        transmission = json.loads(ssl_sock.recv(16384).decode()) #Up to 16KB of data
        
        #If nothing in loaded transmission, retry
        if not transmission:
            break
        
        #Announce newly received target
        header = transmission['header']
        print("'" + header + "' received.")

        #Obtain header to decide appropriate course of action
        #Only accepted headers FROM server TO miner are:
            #MINING COMPLETE
            #NEW TARGET
            
        if(header == "MINING COMPLETE"):
            #Add any mining completes to the global list of mining completes
            gMiningComplete.append(transmission['data'])
            
        elif(header == "NEW TARGET"):
            #A new network target has been recalculated, adjust local targets accordingly
            global target
            target = transmission['data']
            
        else:
            #Unrecognised header
            print("Unrecognised header '" + header + "', discarding transmission.")
        
#Transmitting any data to the server
def transmit(ssl_sock, data, header):
    #Only accepted headers FROM miner TO server are:
        #MINING COMPLETE
    
    #Build transmission as a dict
    transmission = {}
    transmission['data'] = data
    transmission['header'] = header
    
    #Send transmission
    print("Transmitting to server.")
    ssl_sock.send(json.dumps(transmission).encode())   
    
        
#Print out a list of transactions in the working directory that can be mined
def printMinableTransactions():
    print("")
    
    #Transaction files are named with strictly monotonously increasing IDs
    ID = 0
    f = "unminedTransactions/transaction" + str(ID) + ".json"
    
    #While there are still transaction files in the directory
    while(os.path.isfile(f)):
        #Load and print their contents
        with open(f) as fp:
            d = json.load(fp)
        print(json.dumps(d, indent = 4) + "transaction " + str(ID) + "\n")
        
        ID = ID + 1
        f = "unminedTransactions/transaction" + str(ID) + ".json"
        
#Called when the option m is selected form the command line, gets the information required to mine
def getMineInfo():
    #Select a transaction to mine, and load it into a dict for verifying & mining
    ID = input("Input ID of transaction to mine:\n")
    transaction = json.load(open("unminedTransactions/transaction" + str(ID) + ".json"))
    
    #Get the user who will receive the mining reward and store this information to be transmitted
    minerPublicKeyFile = input("Enter name of file in current directory containing public key that this mining effort will be acredited to:\n")
    
    #Get the sender's public key
    srcPublicFile = input("Enter name of file containing sender's known public key for verification:\n")
    
    #Verify if the transaction was legitamitely sent from the given sender by comparing against the message signature          
    if(verifyTransaction(transaction, srcPublicFile)):
        print("The selected transaction has been successfully verified.")
    
        #If verification succeeds, begin the mining process in a new thread, monitor if anyone on the network
        #has already mined the transaction simultaneously, and cancel mining if so
        metrics = {} #count, time, nonce, digest
        metrics['c'] = 0 
        metrics['t'] = 0 
        metrics['n'] = 0
        metrics['d'] = ""
        
        #lambda function used to stop mining thread when appropriate
        stop = False
        global target
        miningThread = threading.Thread(target=mine, args=(transaction, target, metrics, lambda: stop))
        miningThread.start()
        
        #Check that nobody has mined the same transaction
        progress = 0
        progressIcon = ["- ", "\ ", "| ", "/ ", "- ", "\ ", "| ", "/ "]
        
        while(miningThread.isAlive()):
            #Indicate to user that mining is occuring
            print("\rMining " + progressIcon[int(progress/100) % len(progressIcon)], end="")
            progress = progress + 1
            
            for mc in gMiningComplete:
                if mc['transaction'] == transaction:
                    #This means a mining complete signal has already occured for the transaction we are mining
                    stop = True #Will stop the mining thread
                    print("\rAnother miner has completed mining this transaction already;\ncancelling mining & removing transaction from unmined transactions folder.")
                    subprocess.call(["rm", "unminedTransactions/transaction" + str(ID) + ".json"])    #Remove the unsigned message in preparation for next message                    
                    return -1
        
        #Neaten up command line output
        print("\r", end="")
        
        #If out of this loop, must have successfully been the first person on the network to mine transaction
        #Print metrics
        print("Mined w/ nonce " + str(metrics['n']) + " in time: " + str(metrics['t']))    
       
        #Read the key from the file
        minerPublicKey = ""
        for line in open(minerPublicKeyFile, 'r'):
            minerPublicKey = minerPublicKey + line
        
        successfulMine = {}
        successfulMine['miner'] = minerPublicKey
        successfulMine['metrics'] = metrics
        successfulMine['transaction'] = transaction
        
        #Return this information
        return successfulMine 
        
    else:
        #If not verifiable, do not mine as message has been altered with and could be fraudulent
        print("Transaction cannot be verified and will not be mined.") 
        
        #Return symbolic -1 as error     
        return -1

#Repeatedly ran through to get user input
def mainProgramLoop(ssl_sock):
    while(True):
        #Prompt the user to do an action
        instructions  = "Options: \n\t'l' to list names of unverified transactions in working directory by ID, \n\t'm' to select a transaction to mine based on ID, \n\t'q' to quit.\n"
        option = input(instructions)
        while(option != "l" and option != "m" and option != "q"):
            print("Unrecognised option.")
            option = input(instructions)

        #Take action depending on option
        if(option == "l"):
            #List unverified, minable transactions received by the wallet
            printMinableTransactions()
            
        elif(option == "m"):
            #Begin the process of mining, -1 indicates unverifiable or unsuccessfulmine
            info = getMineInfo()
            if(info != -1):
                #Verified and mined
                transmit(ssl_sock, info, "MINING COMPLETE")
                
        elif(option == "q"):
            #Quit
            sys.exit()
        

if __name__ == '__main__':
    #Create a ssl socket connection to server
    ssl_sock = createSSLSocket()
    
    #Start the receiving thread, as we must continuously monitor for incoming messages on the given socket
    receiveThread = threading.Thread(target=receive, args=(ssl_sock,))
    receiveThread.start()
    
    #Enter the main user control loop
    mainProgramLoop(ssl_sock)

    
    

