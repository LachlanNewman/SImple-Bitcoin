import pprint, uuid, subprocess, json, threading, sys
from crypto3002 import *
from blockchain3002 import *
from common3002 import *

unminedTransactionList = [] #Transactions not yet on the blockchain
blockchain = []             #Transactions on the blockchain

#Easiest possible initial target, will mine in one attempt
global target
target = 2**256

#Lachlan Newman
#Isaac Ward
#Receives any data from the server
def receive(ssl_sock, stopRecv):
    #Will be ran as a continuously looping thread that waits for received transmissions
    while not stopRecv():            
        #Load transmission
        transmission = json.loads(ssl_sock.recv(4096).decode()) #Up to 4KB of data
        
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
            #TRANSACTION
            
        if(header == "MINING COMPLETE"):
            #Add any mining completes to the global list of mining completes
            blockchain.append(makeBlock(blockchain, transmission['data']))
            
            #Remove this from the unmined list, as it has now been mined
            t = transmission['data']['transaction']
            if t in unminedTransactionList: unminedTransactionList.remove(t)
            
        elif(header == "NEW TARGET"):
            #A new network target has been recalculated, adjust local targets accordingly
            global target
            target = transmission['data']
        
        elif(header == "TRANSACTION"):
            #A transaction has been observed, add it to the list of unmined transactions
            unminedTransactionList.append(transmission['data'])
            
        else:
            #Unrecognised header
            print("Unrecognised header '" + header + "', discarding transmission.")

#Lachlan Newman
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
    

#Isaac R. Ward
#Print out a list of transactions in the working directory that can be mined
def printMinableTransactions():
    print("")

    #Prints every unmined transaction with ID's increasing monotonically from 0
    ID = 0
    for ut in unminedTransactionList:
        print(json.dumps(ut, indent = 4) + "transaction " + str(ID) + "\n")
        ID = ID + 1
    
    if ID == 0:
        print("There are currently no unmined transactions.\n")
    else:
        print("There are currently " + str(ID) + " unmined transaction(s), with ID's 0 through to " + str(ID - 1) + ".\n")
 
#Isaac R. Ward
#Print out a list of transactions in the working directory that can be mined using file names rather than public keys where possible
def printMinableTransactionsWithFileNames(fileKeyPairs):
    print("")

    #Prints every unmined transaction with ID's increasing monotonically from 0
    ID = 0
    for ut in unminedTransactionList:
        tmpSrcPubKey = ut['srcPubKey']
        tmpDestPubKey = ut['destPubKey']
        
        for p in fileKeyPairs:
            if p['string'] == ut['srcPubKey']:
                ut['srcPubKey'] = p['file']
            if p['string'] == ut['destPubKey']:
                ut['destPubKey'] = p['file']
                
        print(json.dumps(ut, indent = 4) + "transaction " + str(ID) + "\n")
        ID = ID + 1
        
        ut['srcPubKey'] = tmpSrcPubKey
        ut['destPubKey'] = tmpDestPubKey
    
    if ID == 0:
        print("There are currently no unmined transactions.\n")
    else:
        print("There are currently " + str(ID) + " unmined transaction(s), with ID's 0 through to " + str(ID - 1) + ".\n")
 
#Isaac R. Ward  
#Called when the option m is selected form the command line, gets the information required to mine
def mine(minerPublicKey, publicPairList):
    #Select a transaction to mine, and load it into a dict for verifying & mining
    ID = input("Input ID of transaction to mine:\n")    
    if((int(ID) > len(unminedTransactionList) - 1) or not ID.isdigit()):
        #Out of bounds
        print("No transaction matches that ID.\n")
        return -1
        
    transaction = unminedTransactionList[int(ID)]
    
    #Trying to find the sender's public key from the public keys folder
    srcPublicFile = ""
    print("Attempting to locate a public key from the 'publicKeys' folder that matches the sender's public key.")
    for p in publicPairList:
        if p['string'] == transaction['srcPubKey']:
            srcPublicFile = p['file']
    
    #Announce to user that a matching public key was or was not found
    if srcPublicFile == "":
        print("A matching public key could not be found, the message cannot be verified and cannot be mined.")
        return -1
    else:
        print("A matching public key was found in the file: " + srcPublicFile)
        
    #Verify if the transaction was legitamitely sent from the given sender by comparing against the message signature          
    if(verifyTransaction(transaction, "publicKeys/" + srcPublicFile)):
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
        miningThread = threading.Thread(target=proofOfWork, args=(transaction, target, metrics, lambda: stop))
        miningThread.start()
        
        #Check that nobody has mined the same transaction
        progress = 0
        progressIcon = ["- ", "\ ", "| ", "/ ", "- ", "\ ", "| ", "/ "]
        #progressIcon = ["-=======", "=-======", "==-=====", "===-====", "====-===", "=====-==", "======-=", "=======-", "======-=", "=====-==", "====-===", "===-====", "==-=====", "=-======"]
        
        while(miningThread.isAlive()):
            #Indicate to user that mining is occuring
            print("\rMining " + progressIcon[int(progress/100) % len(progressIcon)], end="")
            progress = progress + 1
            
            for b in blockchain:
                if b['transaction'] == transaction:
                    #This means a mining complete signal has already occured for the transaction we are mining
                    stop = True #Will stop the mining thread
                    
                    #Announce outcome to user
                    print("\rAnother miner has completed mining this transaction already;\ncancelling mining & removing transaction from unmined transactions list.")
                    unminedTransactionList.remove(transaction)
                                        
                    return -1
        
        #Neaten up command line output
        print("\r", end="")
        
        #If out of this loop, must have successfully been the first person on the network to mine transaction
        #Print metrics
        print("Mined w/ nonce " + str(metrics['n']) + " in time: " + str(metrics['t']))    
        
        #Announce to user
        print("\rRemoving transaction from unmined transactions list.")
        unminedTransactionList.remove(transaction)
        
        #Add the target at this time to be written into the blockchain
        metrics['target'] = target
        
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
        
#Isaac R. Ward
#Repeatedly ran through to get user input
def mainProgramLoop(ssl_sock, minerPublicKey):
    #Create an dictionary that maps user's public keys to the filenames that they are held in
    publicPairList = getPublicPairs()
    
    for p in publicPairList:
        if p['file'] == minerPublicKey:
            publicKeyString = p['string']

    while(True):
        #Prompt the user to do an action
        instructions  = "Options: \n\t'l' to list unmined transactions by ID, \n\t'lf' to list unmined transactions by ID using .pem filenames in the place of public key strings where possible, \n\t'm' to select a transaction to mine based on ID, \n\t't' to view the target, \n\t'q' to quit.\n"
        option = input(instructions)
        while(option != "l" and option != "m" and option != "q" and option != "lf" and option != "t"):
            print("Unrecognised option.")
            option = input(instructions)

        #Take action depending on option
        if(option == "l"):
            #List unverified, minable transactions received by the wallet
            printMinableTransactions()
        
        elif(option == "lf"):
            #List unmined transactions using filenames where possible
            printMinableTransactionsWithFileNames(publicPairList)
            
        elif(option == "m"):
            #Begin the process of mining, -1 indicates unverifiable or unsuccessfulmine
            info = mine(publicKeyString, publicPairList)
            if(info != -1):
                #Verified and mined
                transmit(ssl_sock, info, "MINING COMPLETE")
                
        elif(option == "t"):
            #User has requested to view the target
            global target   #Using the global target, not creating some local variable
            print("The current network target is:\n" + str(target) + "\nA hash digest LESS THAN this number is required to beat it.\n")
            
        elif(option == "q"):
            #Quit
            break

#Isaac R. Ward
#Gets the public key with which the mines will be accredited with
def getMinerPublicKey():
    #Get the miner's public key base on a file in the public keys file
    instructions  = "Enter the name of the .pem file holding the public key that will be acredited with this session's mines:\n"
    publicKeyFile = input(instructions)
    while not os.path.isfile("publicKeys/" + publicKeyFile):
        print("File not found. Please try again.")
        publicKeyFile = input(instructions)

    return publicKeyFile

#Lachlan Newman
#Isaac R. Ward
if __name__ == '__main__':
    #Create a ssl socket connection to server
    ssl_sock = createSSLSocket()
    
    #Use lambda function to close thread
    stopRecv = False
    
    #Gets the public key with which the mines will be accredited with
    minerPublicKey = getMinerPublicKey()
    
    #Start the receiving thread, as we must continuously monitor for incoming messages on the given socket
    receiveThread = threading.Thread(target=receive, args=(ssl_sock, lambda: stopRecv))
    #Setting a thread to be a daemon ensures it will end when main does
    receiveThread.daemon = True
    receiveThread.start()
    
    #Enter the main user control loop
    mainProgramLoop(ssl_sock, minerPublicKey)
    
    print("Ending user input thread.")
    
    stopRecv = True
    
    print("Ending mining program.")

    sys.exit()

    
    

