import socket, ssl, pprint, uuid, subprocess, json, threading, sys, os
from crypto3002 import *
from blockchain3002 import *
from walletFunctions3002 import *
from common3002 import *

unminedTransactionList = [] #Transactions not yet on the blockchain
blockchain = []             #Transactions on the blockchain

#The coinbase needs to be communicated between threads (reciving thread and main loop) and is thus global, initialised at zero
global coinbase

#Isaac R. Ward
#Prompts the user for input and locates the private and public key files they will use for transacting,
#then reads them into the program
def getUsersKeyPair():
    #Ensure the folder has the correct file structure
    if not os.path.exists("privateKeys"):
        os.makedirs("privateKeys")
    if not os.path.exists("publicKeys"):
        os.makedirs("publicKeys")

    #Prompt the user to 'log in' with their private and public keys
    instructions = "Options: \n\t'e' to use existing keypair, \n\t'n' to generate new key pair.\n"
    option = input(instructions)
    while(option != "e" and option != "n"):
        print("Unrecognised option.")
        option = input(instructions)
    
    #Private will hold the private key as a string, public will hold the public key as a string
    private = ""
    public = ""
    
    #Depending on user option
    if(option == "e"):
        #Gets the file names form the user
        private = input("Enter the name of the .pem file holding your PRIVATE key data in the 'privateKey' directory:\n")
        public = input("Enter the name of the .pem file holding your PUBLIC key data in the 'publicKey' directory:\n")
        
    elif(option == "n"):
        #Generates new files given a symbolic name in the form: "private" + name + ".pem" and "public" + name + ".pem"
        name = input("Enter a symbolic identifier to name your key files with:\n")
        genRSAKeyPairs(name)
        
        #Saves the file names into variables private and public
        private = "private" + name + ".pem"
        public = "public" + name + ".pem"
        
        #Inform user of successful generation
        print("Files created successfully:")
        print("\tPrivate key saved in file private" + name + ".pem in 'privateKeys' directory, keep this file secure!")
        print("\tPublic key saved in file public" + name + ".pem in 'publicKeys' directory.")
        
    return [private, public]

#Lachlan Newman
#Isaac R. Ward
#Receives any data from the server
def receive(ssl_sock, stopRecv):
    #Will be ran as a continuously looping thread that waits for received transmissions
    while not stopRecv():            
        #Load transmission
        transmission = json.loads(ssl_sock.recv(4096).decode()) #Up to 4KB of data
        
        #If nothing in loaded transmission, retry
        if not transmission:
            break

        #Obtain header to decide appropriate course of action
        #Only accepted headers FROM server TO client are:
            #TRANSACTION
            #MINING COMPLETE
        
        #Announce transmission received
        header = transmission['header']
        print("'" + header + "' received.")
        
        if(header == "TRANSACTION"):
            #The received transmission is a transaction, strip the header and save the transaction to a global list
            unminedTransactionList.append(transmission['data'])
                
        elif(header == "MINING COMPLETE"):
            #A miner has successfully mined a transaction, it needs to be written to the blockchain and removed from the unmined list
            blockchain.append(makeBlock(blockchain, transmission['data']))
            
            t = transmission['data']['transaction']
            if t in unminedTransactionList: unminedTransactionList.remove(t)
        
        elif(header == "NEW COINBASE"):
            #The server is issuing a network wide coinbase
            global coinbase
            coinbase = int(transmission['data'])
            
        else:
            #Unrecognised header
            print("Unrecognised header '" + header + "', discarding transmission.")
    
    print("Ending transmission recieval thread.")
        
#Lachlan Newman
#Transmitting any data to the server
def transmit(ssl_sock, data, header):
    #Only accepted headers FROM client TO server are:
        #TRANSACTION
        #CLIENT SIGNAL
    
    #Build transmission as a dict
    transmission = {}
    transmission['data'] = data
    transmission['header'] = header
    
    #For testing purposes
    confirmation = input("Transmitting following transaction:\n\n" + json.dumps(transmission, indent = 4) + "\n\nConfirm? (y/n)\n")

    #Transmit to server
    if(confirmation == "y"):
        print("Transmitting...")
        #Send transmission
        ssl_sock.send(json.dumps(transmission).encode())   
    else:
        print("Cancelling transaction.")

#Isaac R. Ward
#Creates a transaction with another user
def transact(srcPrivate, srcPublic):
    #Get the destination public key
    instructions  = "Enter the name of the .pem file holding the receiver's PUBLIC key data in current directory:\n"
    destPublic = input(instructions)
    
    #Get the amount the user wishes to send as an integer
    instructions = "Enter the (integer) number of coins you wish to send to the receiver:\n"
    amount = input(instructions)
    while(not amount.isdigit() or int(amount) < 0):
        print("Non integer and negative amounts are not recognised.\n")
        amount = input(instructions)
        
    #First check if the you have the requierd amount by looking over the blockchain
    srcPublicString = ""
    for line in open("publicKeys/" + srcPublic, 'r'):
        srcPublicString = srcPublicString + line
    
    #Check balances using the global server issued coinbase value
    global coinbase
    if(checkBalance(blockchain, srcPublicString, coinbase) < int(amount)):
        print("You do not have the required amount to send.")
        return -1
    
    #Build a signed transaction
    m = buildTransaction("privateKeys/" + srcPrivate, "publicKeys/" + srcPublic, "publicKeys/" + destPublic, amount)
    return m

#Isaac R. Ward
#Main user input loop   
def mainProgramLoop(userPrivate, userPublic, ssl_sock):
    #List of dictionaries that hold public key file names and public key strings as pairs
    publicPairList = []     
    publicPairList = getPublicPairs()

    while(True):
        #Prompt the user to do an action
        instructions  = "Options: \n\t'r' to read ane changes to the 'publicKeys' folder, \n\t't' to transact with another user, \n\t'b' to view the blockchain, \n\t'bf' to view the blockchain with .pem file names instead of key strings (based off the contents of the 'publicKeys' folder), \n\t'bs' to save the current blockchain to a folder in the program's directory, \n\t'c' to check the balances of all known users, \n\t'q' to quit.\n"
        option = input(instructions)
        while(option != "r" and option != "t" and option != "q" and option != "b" and option != "bf" and option != "bs" and option != "c"):
            print("Unrecognised option.")
            option = input(instructions)
        
        #Execute appropriate function depending on option
        if(option == "q"):
            #Quit
            break
            
        elif(option == "r"):
            #Re read the publicKeys folder
            publicPairList = getPublicPairs();
            
        elif(option  == "t"):
            #Transact
            #Build a signed transaction with user input
            t = transact(userPrivate, userPublic)
            #Send transaction to server to be retransmitted to network
            if(t != -1):
                transmit(ssl_sock, t, "TRANSACTION")

        elif(option == "b"):
            #View blockchain
            printBlockchain(blockchain)
            
        elif(option == "bf"):
            #View blockchain with file names in the place of key strings when possible
            printBlockchainWithFileNames(blockchain, publicPairList)
            
        elif(option == "bs"):
            #Save the current block chain to a folder
            saveBlockChain(blockchain)
            
        elif(option == "c"):
            #View all known user's balances
            for u in publicPairList:
                global coinbase #Use the global server issued coinbase to evaulate mining rewards (50 by default)
                userBalance = checkBalance(blockchain, u['string'], coinbase)
                print("\t" + u['file'] + " has balance: " + str(userBalance))
                
            print("")            

#Lachlan Newman
#Execution begins here
if __name__ == '__main__':
    #Create a ssl socket connection to server
    ssl_sock = createSSLSocket()
    
    #Get key pair filenames into variables
    privateFile, publicFile = getUsersKeyPair()
    #print(privatekey)
    #print(publickey)
    
    #lambda function used to stop the recieve thread when user specifies quit
    stopRecv = False
    
    #Start the receiving thread, as we must continuously monitor for incoming messages on the given socket
    receiveThread = threading.Thread(target=receive, args=(ssl_sock, lambda: stopRecv))
    #Setting a thread to be a daemon ensures it will end when main does
    receiveThread.daemon = True
    receiveThread.start()

    #Enter the main user control loop, only exiting by specifying quit, which will then stop the receive thread
    mainProgramLoop(privateFile, publicFile, ssl_sock)
    print("Ending user input thread.")
    
    stopRecv = True #Stops recieve thread

    print("Ending wallet program.")

    sys.exit()
    

