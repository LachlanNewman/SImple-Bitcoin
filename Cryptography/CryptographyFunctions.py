#Isaac R. Ward
#Run on linux with 'python3 CryptographyFunctions.py'

from subprocess import call         #For calling OpenSSL command line functions
import subprocess

import hashlib                      #For SHA256

import random                       #For generating nonces
import string

import time                         #For timing nonce finding

import json

#Generates RSA key pairs with specified bit modulus into encrypted PEM files
#named privateX.pem & publicX.pem using OpenSSL command line functions the
#program is thus dependant on the OpenSSL program library and it must be
#ensured that this is installed prior
def genRSAKeyPairs(bitModulus, ID):
    #Use OpenSSL to generate given bit modulus RSA keys NOT using Triple Data Encryption (-des3)
    call(["openssl", "genrsa", "-out", "private" + ID + ".pem", bitModulus])
    
    #Write public key out to new file named publicX.pem
    call(["openssl", "rsa", "-in", "private" + ID + ".pem", "-outform", "PEM", "-pubout", "-out", "public" + ID + ".pem"])

    '''
    #Print out to command line
    print("For ID " + ID + "{\n")
    
    for line in open("private" + ID + ".pem", 'r'):
        print(line)

    for line in open("public" + ID + ".pem", 'r'):
        print(line)

    print("}\n\n")
    '''
    
    

#Builds a transaction message that src will send to dest which includes:
    #-src's public key
    #-dest's public key
    #-transaction details (amount being sent etc)
    #-digital signature based off of src's private key (fraud proofing)
def buildTransactionMessage(srcID, destID, transactionDetails):
    #Concat src's public key, dest's public key
    message = srcID + "'s PUBLIC KEY\n"
    
    for line in open("public" + srcID + ".pem", 'r'):
        #Drop headers
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            message = message + line

    message = message + destID + "'s PUBLIC KEY\n"

    for line in open("public" + destID + ".pem", 'r'):
        #Drop headers
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            message = message + line

    #Concat transaction details
    message = message + "TRANSACTION DETAILS\n"
    message = message + transactionDetails + "\n"
    
    #Calculate digital signature based of SHA256 of transaction details encrypted with
    #src's private key and append to message

    unsignedMessage = open(srcID + "->" + destID + "-Unsigned.txt", "w")
    unsignedMessage.write(message)
    unsignedMessage.close()
    
    call(["openssl", "dgst", "-sha256",                     #SHA256 signature
                  "-sign", "private" + srcID + ".pem",      #Using sources private key
                  "-out", "tmpSignature",                   #Save temporarily as tmpSignature
                  srcID + "->" + destID + "-Unsigned.txt"]) #File to sign
    
    call(["openssl", "base64",                                      #Convert to base64
                  "-in", "tmpSignature",                            #Converting just generated signature^
                  "-out", srcID + "->" + destID + "-Signature.txt"])#File containing signature
    
    call(["rm", "tmpSignature"])
    #call(["rm", srcID + "->" + destID + "-Unsigned.txt"])

    message = message + "SIGNATURE\n"
    for line in open(srcID + "->" + destID + "-Signature.txt", "r"):
        message = message + line
    

    #Output final message to txt file named srcID->destID
    file = open(srcID + "->" + destID + "-Signed.txt", "w")
    file.write(message)
    file.close()

#For verifying signature using OpenSSL command line functions
def verifyTransactionMessage(fileName):
    print("Verifying transaction '%s'..." % fileName)

    srcID = fileName[0]     #This is lazy, should use file contents
    destID = fileName[3]

    #https://gist.github.com/ezimuel/3cb601853db6ebc4ee49
    call(["openssl", "base64", "-d",                                 #Convert from base64
                  "-in", srcID + "->" + destID + "-Signature.txt",   #The message's signature
                  "-out", "tmpSignature"])                           #Into a temporary binary file

    p = subprocess.Popen(["openssl", "dgst", "-sha256", "-verify",   #Verify and capture OpenSSL console output
                  "public" + srcID + ".pem",                         #Using src's public key
                  "-signature", "tmpSignature",                      #Against the message's signature
                  srcID + "->" + destID + "-Unsigned.txt"],            #To verify the unsigned message
		  stdout=subprocess.PIPE).communicate()[0]
    
    call(["rm", "tmpSignature"])
    
    if(p != "Verification Failure\n"):
        return True
    	
    return False

#Miner's proof of work algorithm
def proofOfWork(messageName):
    message = ""
    
    for line in open(messageName, 'r'):
        message = message + line

    #Put message as initial string into hash object
    minersHash = hashlib.sha256()
    minersHash.update(str(random.randint(0, 999999)).encode(encoding='UTF-8'))
    #minersHash.update(message.encode(encoding='UTF-8'))

    #Begin mining
    start = time.time()
    count = 0

    #Testing all 16 digit integer nonces
    for nonce in range(0, 10**16):
        minersHashCopy = minersHash.copy()
        minersHashCopy.update(repr(nonce).encode('UTF-8'))
        hash = minersHashCopy.hexdigest()
        count = count + 1

        #Need first x digits of guess to be greater than difficulty
        if(int(hash, 16) < target):
            end = time.time()
            timeTaken = end - start
            print("Crypto hash cracked in " + str(count) + " hashes w/ nonce " + str(nonce) + " in time: " + str(timeTaken))
            
            return timeTaken

    #Add this nonce to the transaction message
    with open(messageName, 'a') as messageFile:
        messageFile.write("NONCE\n")
        messageFile.write(nonce)
    
#Dict message builder
def buildTransactionDict(srcID, destID, transactionDetails):
    call(["rm", "tmpSignature.pem"])            #Remove holder files incase there was an interruption
    call(["rm", "unsignedMessage.json"])    #and they are still in the active folder
    
    #Get the src's public key into a string src w/o newlines and carriage returns
    src = ""
    for line in open("public" + srcID + ".pem", 'r'):
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            src = src + line.rstrip('\r\n')

    #Get the dest's public key into a string dest w/o newlines and carriage returns
    dest = ""
    for line in open("public" + srcID + ".pem", 'r'):
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            dest = dest + line.rstrip('\r\n')

    #Generate the unsigned message as a json file
    unsignedMessage = {}
    unsignedMessage['srcPubKey'] = src
    unsignedMessage['srcID'] = srcID
    unsignedMessage['desPubKey'] = dest
    unsignedMessage['destID'] = destID
    unsignedMessage['transaction'] = transactionDetails

    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp, indent = 4)
        
    #Generate the signature for this unsigned message
    call(["openssl", "dgst", "-sha256",                     #SHA256 signature
                  "-sign", "private" + srcID + ".pem",      #Using sources private key
                  "-out", "tmpSignature.pem",               #Save temporarily as tmpSignature
                  "unsignedMessage.json"])                  #File to sign

    call(["rm", "unsignedMessage.json"])    #Remove the unsigned message in preparation for next message
    
    call(["openssl", "base64",                      #Convert to base64
                  "-in", "tmpSignature/pem",        #Converting just generated signature^
                  "-out", "signature.pem"])         #File containing signature

    #Get the message's signature into a string w/o newlines and carriage returns
    sig = ""
    for line in open("signature.pem", 'r'):
        sig = sig + line.rstrip('\r\n')
    
    call(["rm", "tmpSignature"])    #Remove the signature file in preparation for the next message

    #Construct the final, signed message
    signedMessage = {}

    signedMessage['srcPubKey'] = src
    signedMessage['srcID'] = srcID
    signedMessage['desPubKey'] = dest
    signedMessage['destID'] = destID
    signedMessage['signature'] = sig
    signedMessage['transaction'] = transactionDetails
    signedMessage['verified'] = False

    with open('signedMessage.json', 'w') as fp:
        json.dump(signedMessage, fp, indent = 4)

    return signedMessage
    
#For verifying incoming message dicts with OpenSSL command line functions
def verifyTransactionDict(unverifiedMessage):
    call(["rm", "sig.pem"])   #Remove holder files incase there was an interruption
    call(["rm", "unsignedMessage.json"])
    call(["rm", "tmpSignature.pem"])

    #Write the signature to a file for OpenSSL
    sig = open("sig.pem", "w")
    sig.write(unverifiedMessage['signature'])

    #Write the rest of the message to a file for OpenSSL
    unsignedMessage = {}
    unsignedMessage['srcPubKey'] = unverifiedMessage['srcPubKey']
    unsignedMessage['destPubKey'] = unverifiedMessage['destPubKey']
    unsignedMessage['transaction'] = unverifiedMessage['transaction']
    
    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp, indent = 4)

    #The verification process
    call(["openssl", "base64", "-d",        #Convert from base64
                  "-in", "sig.pem",         #The message's signature
                  "-out", "tmpSignature.pem"])  #Into a temporary binary file

    p = subprocess.Popen(["openssl", "dgst", "-sha256", "-verify",   #Verify and capture OpenSSL console output
                  "public" + unsignedMessage['srcID'] + ".pem",      #Using src's public key on local system
                  "-signature", "tmpSignature.pem",                  #Against the message's signature
                  "unsignedMessage.json"],                           #To verify the unsigned message
		  stdout=subprocess.PIPE).communicate()[0]

    call(["rm", "sig.pem"])   #Remove holder files in preparation for next verification
    call(["rm", "unsignedMessage.json"])
    call(["rm", "tmpSignature.pem"])
    
    #If not a failure, must be a success -> verified
    if(p != "Verification Failure\n"):
        unverifiedMessage['verified'] = True
        print("Verified!")
    	
    return unverifiedMessage


#Main code
if __name__ == '__main__':
    #In the wallet, generate info for two users and construct a message and send
    genRSAKeyPairs("2048", "A")
    genRSAKeyPairs("2048", "B")
    #buildTransactionMessage("A", "B", "~~~TRANSACTION DETAILS PLACEHOLDER~~~")
    verifyTransactionDict(buildTransactionDict("A", "B", "~~~TRANSACTION DETAILS PLACEHOLDER~~~"))
    


    global target				#Integer that hash needs to be less than 
    target = 2**256
    #(hard) 0 < target < 2**256 (easy)

    totaltime = 0.0

    while(True):
        timelog = []
    	#In the miner, do proof of work algorithm on given message, this new message is sent to all users
        for i in range(0,9):
            timelog.append(proofOfWork("A->B-Signed.txt"))
    	
        totaltime = sum(timelog)
        target = int(target/(120*10/totaltime))
	
        print("Total time to crack hashes: " + str(totaltime) + ", \nnew difficulty = " + str(target))

    """
    #In other wallet, verify signed message and add information to block chain
    if verifyTransactionMessage("A->B-Signed") == True:
        print("Verification successful")
    else:
        print("Verification failure")
    """
    
