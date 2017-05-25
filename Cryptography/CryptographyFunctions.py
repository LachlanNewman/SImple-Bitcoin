#Isaac R. Ward

from subprocess import call         #For calling OpenSSL command line functions
import subprocess

import hashlib                      #For calculating SHA256
import time                         #For timing nonce finding

import json							#For dumping dicts

#Generates RSA key pairs with specified bit modulus into encrypted PEM files
#named privateX.pem & publicX.pem using OpenSSL command line functions the
#program is thus dependant on the OpenSSL program library and it must be
#ensured that this is installed prior
def genRSAKeyPairs(ID):
    #Use OpenSSL to generate given bit modulus RSA keys NOT using Triple Data Encryption (-des3)
    call(["openssl", "genrsa", "-out", "private" + ID + ".pem", "2048"])
    
    #Write public key out to new file named publicX.pem
    call(["openssl", "rsa", "-in", "private" + ID + ".pem", "-outform", "PEM", "-pubout", "-out", "public" + ID + ".pem"])    

#Miner's proof of work algorithm on a message dict
#Returns the number of attempts, timeTaken, nonce and digest
def proofOfWork(message, target):
    #Put message dict in string representation into hash object initially
    minersHash = hashlib.sha256()
    minersHash.update((json.dumps(message)).encode(encoding='UTF-8'))

    #Begin mining
    start = time.time()
    count = 0

    #Testing all 16 digit integer nonces
    for nonce in range(0, 10**16):
        #Add the nonce into a copy of the hash
        minersHashCopy = minersHash.copy()
        minersHashCopy.update(repr(nonce).encode('UTF-8'))
        hash = minersHashCopy.hexdigest()
        count = count + 1

        #Need digest's value to beat a given network target
        if(int(hash, 16) < target):
            #If so log various statistics
            end = time.time()
            timeTaken = end - start

            #Return timeTaken, nonce and digest
            return [count, timeTaken, nonce, hash]

    
#For building signed messaged from srcID to destID with the given amount
#Returns the transaction in signed dict format
def buildTransactionDict(srcID, destID, transaction):
    #Get the src's public key into a string src w/o newlines and carriage returns
    src = ""
    for line in open("public" + srcID + ".pem", 'r'):
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            src = src + line.rstrip('\r\n')

    #Get the dest's public key into a string dest w/o newlines and carriage returns
    dest = ""
    for line in open("public" + destID + ".pem", 'r'):
        if(line != "-----BEGIN PUBLIC KEY-----\n" and line != "-----END PUBLIC KEY-----\n"):
            dest = dest + line.rstrip('\r\n')

    #Generate the unsigned message as a json file
    unsignedMessage = {}
    unsignedMessage['srcPubKey'] = src
    unsignedMessage['srcID'] = srcID
    unsignedMessage['destPubKey'] = dest
    unsignedMessage['destID'] = destID
    unsignedMessage['transaction'] = transaction

    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp, indent = 4)
        
    #Generate the signature for this unsigned message
    call(["openssl", "dgst", "-sha256",                     #SHA256 signature
                  "-sign", "private" + srcID + ".pem",      #Using sources private key
                  "-out", "sigBin",               #Save temporarily as binSig
                  "unsignedMessage.json"])                  #File to sign

    call(["rm", "unsignedMessage.json"])    #Remove the unsigned message in preparation for next message
    
    call(["openssl", "base64", "-e",             #Convert to base64
                  "-in", "sigBin",        #Converting just generated signature^
                  "-out", "sig64"])         #File containing signature

    call(["rm", "sigBin"])    #Remove the binary representation of the signature

    #Get the message's signature into a string WITH newlines and carriage returns as OpenSSL requires them for decoding
    sig = ""
    for line in open("sig64", 'r'):
        sig = sig + line

    call(["rm", "sig64"])    #Remove the base64 representation of the signature


    #Construct the final, signed message
    signedMessage = {}

    signedMessage['srcPubKey'] = src
    signedMessage['srcID'] = srcID
    signedMessage['destPubKey'] = dest
    signedMessage['destID'] = destID
    signedMessage['signature'] = sig
    signedMessage['transaction'] = transaction
    signedMessage['verified'] = False

    #with open('signedMessage.json', 'w') as fp:
        #json.dump(signedMessage, fp, indent = 4)

    return signedMessage
    
#For verifying incoming message dicts with OpenSSL command line functions
#Returns the given message with the verified field altered accordingly
def verifyTransactionDict(unverifiedMessage):
    #Write the signature to a file for OpenSSL
    sig = open("sig64", "w")
    sig.write(unverifiedMessage['signature'])
    sig.close()

    #Write the rest of the message to a file for OpenSSL
    unsignedMessage = {}
    unsignedMessage['srcPubKey'] = unverifiedMessage['srcPubKey']
    unsignedMessage['srcID'] = unverifiedMessage['srcID']
    unsignedMessage['destPubKey'] = unverifiedMessage['destPubKey']
    unsignedMessage['destID'] = unverifiedMessage['destID']
    unsignedMessage['transaction'] = unverifiedMessage['transaction']
    
    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp, indent = 4)
    fp.close()

    #The verification process
    print("Verifying")
    call(["openssl", "base64", "-d",       #Convert from base64
                  "-in", "sig64",        #The message's signature
                  "-out", "sigBin"])  #Into a temporary binary file

    call(["rm", "sig64"])    #Remove the base64 representation of the signature

    p = subprocess.Popen(["openssl", "dgst", "-sha256", "-verify",   #Verify and capture OpenSSL console output
                  "public" + unsignedMessage['srcID'] + ".pem",      #Using src's public key on local system
                  "-signature", "sigBin",                  #Against the message's signature
                  "unsignedMessage.json"],                           #To verify the unsigned message
		  stdout=subprocess.PIPE).communicate()[0]

    call(["rm", "sigBin"])    #Remove the binary representation of the signature
    call(["rm", "unsignedMessage.json"])    #Remove the unsigned message in preparation for next message

    #If verified OK is present in command line return, must be a success -> verified
    if("Verified OK" in str(p)):
        unverifiedMessage['verified'] = True
        print("Verified!")
    else:
        print("Not verified!")

    #Otherwise message remains with verified = false
    return unverifiedMessage
