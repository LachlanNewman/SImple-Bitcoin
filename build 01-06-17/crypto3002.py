import subprocess       #For calling OpenSSL command line functions & command line output
import hashlib          #For calculating SHA256
import time             #For timing nonce finding
import json				#For dumping dicts
import collections      #For ordering dicts
import os               #For removing files

#Isaac R. Ward
#Generates RSA key pairs with specified location into encrypted PEM files
#named privateID.pem & publicID.pem using OpenSSL command line functions the
#program is thus dependant on the OpenSSL program library and it must be
#ensured that this is installed prior
def genRSAKeyPairs(ID):
    #Use OpenSSL to generate given bit modulus RSA keys NOT using Triple Data Encryption (-des3)
    subprocess.call(["openssl", "genrsa", "-out", "privateKeys/private" + ID + ".pem", "2048"])
    
    #Write public key out to new file named publicX.pem
    subprocess.call(["openssl", "rsa", "-in", "privateKeys/private" + ID + ".pem", "-outform", "PEM", "-pubout", "-out", "publicKeys/public" + ID + ".pem"])    

#Isaac R. Ward
#Miner's proof of work algorithm on a message dict
#Returns the number of attempts, timeTaken, nonce and digest
def proofOfWork(message, target, metrics, stop):
    #Put message dict in string representation into hash object initially
    minersHash = hashlib.sha256()
    minersHash.update((json.dumps(message)).encode(encoding='UTF-8'))

    #Begin mining from nonce 0 upwards
    start = time.time()
    count = 0
    nonce = 0
    mined = False
    
    #While haven't successfully mined and haven't been instructed to terminate the mining thread
    while not stop() and not mined:
        #Add the nonce into a copy of the hash
        minersHashCopy = minersHash.copy()
        minersHashCopy.update(repr(nonce).encode('UTF-8'))
        digest = minersHashCopy.hexdigest()
        count = count + 1

        #Need digest's value to beat a given network target
        if(int(digest, 16) < target):        
            #If so log various statistics
            end = time.time()
            timeTaken = end - start

            #Return count, timeTaken, nonce and digest
            metrics['c'] = count
            metrics['t'] = timeTaken
            metrics['n'] = nonce
            metrics['d'] = digest
            
            mined = True
            
            #For testing
            #print("Writing metrics: " + str(metrics))
        
        #Try a new nonce
        nonce = nonce + 1

#Isaac R. Ward
#For building signed messaged from srcID to destID with the given amount
#Returns the transaction in signed dict format
def buildTransaction(srcFilePrivate, srcFilePublic, destFilePublic, amount):
    #Get the src's public key into a string src w/ headers, newlines and carriage returns
    src = ""
    for line in open(srcFilePublic, 'r'):
        src = src + line
        
    #Get the dest's public key into a string dest w/ headers, newlines and carriage returns
    dest = ""
    for line in open(destFilePublic, 'r'):
        dest = dest + line

    #Generate the unsigned message as required by the project specifications before signing as a json file (order is important)
    unsignedMessage = collections.OrderedDict()
    unsignedMessage['srcPubKey'] = src
    unsignedMessage['destPubKey'] = dest
    unsignedMessage['amount'] = amount

    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp)
    fp.close()
        
    #Generate the signature for this unsigned message
    subprocess.call(["openssl", "dgst", "-sha256",  #SHA256 signature
                     "-sign", srcFilePrivate,       #Using sources private key
                     "-out", "sigBin",              #Save temporarily as binSig
                     "unsignedMessage.json"])       #File to sign

    os.remove("unsignedMessage.json")    #Remove the unsigned message in preparation for next message
    
    subprocess.call(["openssl", "base64", "-e",     #Convert to base64
                     "-in", "sigBin",               #Converting just generated signature^
                     "-out", "sig64"])              #File containing signature

    os.remove("sigBin")    #Remove the binary representation of the signature

    #Get the message's signature into a string WITH newlines and carriage returns as OpenSSL requires them for decoding
    sig = ""
    for line in open("sig64", 'r'):
        sig = sig + line

    os.remove("sig64")    #Remove the base64 representation of the signature


    #Construct the final, signed message, again, in order
    signedMessage = collections.OrderedDict()
    
    signedMessage['srcPubKey'] = src
    signedMessage['destPubKey'] = dest
    signedMessage['amount'] = amount
    signedMessage['signature'] = sig

    #For viewing signed messages created by this function
    #with open('signedMessage.json', 'w') as fp:
        #json.dump(signedMessage, fp, indent = 4)

    return signedMessage

#Isaac R. Ward
#For verifying incoming message dicts with OpenSSL command line functions
#Returns the given message with the verified field altered accordingly
def verifyTransaction(unverifiedMessage, srcPublicFile):

    #Write the signature to a file for OpenSSL
    sig = open("sig64", "w")
    sig.write(unverifiedMessage['signature'])
    sig.close()

    #Write the rest of the message to a file for OpenSSL
    unsignedMessage = collections.OrderedDict()
    unsignedMessage['srcPubKey'] = unverifiedMessage['srcPubKey']
    unsignedMessage['destPubKey'] = unverifiedMessage['destPubKey']
    unsignedMessage['amount'] = unverifiedMessage['amount']
    
    with open('unsignedMessage.json', 'w') as fp:
        json.dump(unsignedMessage, fp)
    fp.close()

    #The verification process
    #print("Verifying")
    subprocess.call(["openssl", "base64", "-d",     #Convert from base64
                     "-in", "sig64",                #The message's signature
                     "-out", "sigBin"])             #Into a temporary binary file

    os.remove("sig64")    #Remove the base64 representation of the signature

    p = subprocess.Popen(["openssl", "dgst", "-sha256", "-verify",  #Verify and capture OpenSSL console output
                          srcPublicFile,                            #Using src's public key on local system
                          "-signature", "sigBin",                   #Against the message's signature
                          "unsignedMessage.json"],                  #To verify the unsigned message
	      stdout=subprocess.PIPE).communicate()[0]

    os.remove("sigBin")                 #Remove the binary representation of the signature
    os.remove("unsignedMessage.json")   #Remove the unsigned message in preparation for next message

    #If "Verified OK" is present in command line return then the verification process must have succeeded, edit message accordingly
    if("Verified OK" in str(p)):
        #print("Verified!")
        return True
    else:
        #Otherwise message remains unverified
        #print("Not verified!")
        return False
