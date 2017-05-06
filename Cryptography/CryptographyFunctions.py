#Isaac R. Ward
#Run on linux with 'python3 CryptographyFunctions.py'

from subprocess import call         #For calling OpenSSL command line functions
import subprocess

import hashlib                      #For SHA256

import random                       #For generating nonces
import string

import time                         #For timing nonce finding

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
    minersHash.update(message.encode(encoding='UTF-8'))

    #While the first byte is not '00000000' in bits, try another random nonce appended to the original message
    print("Doing proof of work on transaction message from" + messageName + "...")
    start = time.time()
    count = 1
    
    nonce = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))
    minersHashCopy = minersHash.copy()
    minersHashCopy.update(nonce.encode(encoding='UTF-8'))

    difficulty = 17      #How many leading digits of bit hash (not hex hash) are required to be 0 for success
    while('{:0256b}'.format(int(minersHashCopy.hexdigest(), 16))[:difficulty].count("0") != difficulty):
        #Reload the hash copy with the transaction message in it and attempt the hash with a new 8 letter nonce
        nonce = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))
        minersHashCopy = minersHash.copy()
        minersHashCopy.update(nonce.encode(encoding='UTF-8'))
        count = count + 1
        print("\rNonce: '%s' yields first %d bits of hash: '%s'." % (nonce, difficulty, '{:0256b}'.format(int(minersHashCopy.hexdigest(), 16))[:difficulty]), end="")

    end = time.time()
    timeTaken = str(end - start)
    print("\nCorrect nonce found in %d hashes, time taken: %s seconds" % (count, timeTaken))
    
    #Add this nonce to the transaction message ready to be written to the blockchain & THEN sent to src & dest
    with open(messageName, 'a') as messageFile:
        messageFile.write("NONCE\n")
        messageFile.write(nonce)
	


#Main code
if __name__ == '__main__':
    #In the wallet, generate info for two users and construct a message and send
    genRSAKeyPairs("2048", "A")
    genRSAKeyPairs("2048", "B")
    buildTransactionMessage("A", "B", "~~~TRANSACTION DETAILS PLACEHOLDER~~~")

    #In the miner, do proof of work algorithm on given message, this new message is sent to all users
    proofOfWork("A->B-Signed.txt")

    #In other wallet, verify signed message and add information to block chain
    if verifyTransactionMessage("A->B-Signed") == True:
        print("Verification successful")
    else:
        print("Verification failure")
    
