import socket, ssl, pprint, uuid, subprocess, json, threading, sys, os
from crypto3002 import *

global transactionList
transactionList = []

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

def getUsersKeyPair():
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
        private = input("Enter the name of the .pem file holding your PRIVATE key data in current directory:\n")
        public = input("Enter the name of the .pem file holding your PUBLIC key data in current directory:\n")
        
    elif(option == "n"):
        #Generates new files given a symbolic name in the form: "private" + name + ".pem" and "public" + name + ".pem"
        name = input("Enter a symbolic identifier to name your key files with:\n")
        genRSAKeyPairs(name)
        
        #Saves the file names into variables private and public
        private = "private" + name + ".pem"
        public = "public" + name + ".pem"
        
        #Inform user of successful generation
        print("Files created successfully:")
        print("\tPrivate key saved in file private" + name + ".pem, keep this file secure!")
        print("\tPublic key saved in file public" + name + ".pem.")
        
    return [private, public]

#Prints visual representation of the wallet
def printWallet():
    #TODO
    print("The wallet is as follows:")

#Prints visual representation of the blockchain
def printBlockchain():
    #TODO
    print("The blockchain is as follows:")

#Receives any data from the server
def receive(ssl_sock):
    #Will be ran as a continuously looping thread that waits for received transmissions
    while(True):            
        #Load transmission
        transmission = json.loads(ssl_sock.recv(16384).decode()) #Up to 16KB of data
        
        #If nothing in loaded transmission, retry
        if not transmission:
            break

        #Obtain header to decide appropriate course of action
        #Only accepted headers FROM server TO client are:
            #TRANSACTION
            #TRANSACTIONS READOUT
            
        header = transmission['header']
        if(header == "TRANSACTION"):
            #The received transmission is a transaction, strip the header and save the transaction to a global list
            #Dump to a file to allow mining
            transactionList.append(transmission['data'])
            #with open('signedMessage.json', 'w') as fp:
                #json.dump(signedMessage, fp, indent = 4)

        else:
            #Unrecognised header
            print("Unrecognised header '" + header + "', discarding transmission.")
        
    
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

#Creates a transaction with another user
def transact(srcPrivate, srcPublic):
    #Get the destination public key
    instructions  = "Enter the name of the .pem file holding the receiver's PUBLIC key data in current directory:\n"
    destPublic = input(instructions)
    
    #Get the amount the user wishes to send as an integer
    instructions = "Enter the (integer) number of coins you wish to send to the receiver:\n"
    amount = input(instructions)
    while(not amount.isdigit()):
        print("Non integer amounts are not recognised.\n")
        amount = input(instructions)
    
    #Build a signed transaction
    m = buildTransaction(srcPrivate, srcPublic, destPublic, amount)
    return m
    
    
def mainProgramLoop(userPrivate, userPublic, ssl_sock):
    while(True):
        #Prompt the user to do an action
        instructions  = "Options: \n\t't' to transact with another user, \n\t'p' to print all observed network transactions during this connection, \n\t's' to save all observed network transactions into the working directory for mining\n\t'w' to view wallet data, \n\t'b' to view blockchain data, \n\t'q' to quit.\n"
        option = input(instructions)
        while(option != "t" and option != "q" and option != "w" and option != "b" and option != "p" and option != "s"):
            print("Unrecognised option.")
            option = input(instructions)
        
        #Execute appropriate function depending on option
        if(option == "q"):
            #Quit
            sys.exit()
            
        elif(option  == "t"):
            #Transact
            #Build a signed transaction with user input
            t = transact(userPrivate, userPublic)
            #Send transaction to server to be retransmitted to network
            transmit(ssl_sock, t, "TRANSACTION")
            
        elif(option == "w"):
            #View wallet
            printWallet()
            
        elif(option == "p"):
            #Print all transactions observed
            print(json.dumps(transactionList, indent = 4))
            
        elif(option == "b"):
            #View blockchain
            printBlockchain()
            
        elif(option == "s"):
            #Save each transactions in the global list to json file in a new folder called 'transactions'. Create this folder if it doesn't already exist
            transactionsDir = os.path.join(os.getcwd(), r'unminedTransactions')
            if(not os.path.exists(transactionsDir)):
                os.mkdir(transactionsDir)
                
            #Begin saving transactions in arbitrary order
            ID = 0
            for t in transactionList:
                with open("unminedTransactions/transaction" + str(ID) + ".json", 'w') as fp:
                    #Remove old contents
                    fp.seek(0)
                    fp.truncate()
                    
                    #And insert new
                    json.dump(t, fp)
                    
                ID = ID + 1
            print(str(ID) + " transaction(s) saved into unmined transactions folder.")
    
if __name__ == '__main__':
    #Create a ssl socket connection to server
    ssl_sock = createSSLSocket()
    
    #Get key pair filenames into variables
    privateFile, publicFile = getUsersKeyPair()
    #print(privatekey)
    #print(publickey)
    
    #Start the receiving thread, as we must continuously monitor for incoming messages on the given socket
    receiveThread = threading.Thread(target=receive, args=(ssl_sock,))
    receiveThread.start()  

    #Enter the main user control loop
    mainProgramLoop(privateFile, publicFile, ssl_sock)

    
    

