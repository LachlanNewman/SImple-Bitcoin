import socket, ssl, pprint, uuid, subprocess, json

#TODO make headers in messages to differentiate between
#       -publickeys
#       -transactions
#       -mining signalsfor conn in clientConnections:   
#       others??

#------------------------------------------------------------------------------------------------------------------------------------------
#sends all transactions to server TODO EXPLAIN MORE
#------------------------------------------------------------------------------------------------------------------------------------------
def sendTransaction(ssl_sock,userid):
    while True:
        transaction = {}                        #empty transaction
        src         = userid                    #auto userid of sender
        dest        = input("id:"       )       #user id of reciever
        amount      = input("amount:"   )       #amount to transfer
        comment     = input("comment:"  )       #comment to go with transaction
        if src == "X" and dest =="X" and amount = "X":          #condition to end socket connection TODO add to readme file
            break;
        ssl_sock.write(message.encode())        #send transaction to server

#------------------------------------------------------------------------------------------------------------------------------------------
#get all the publickeys of users in the network #TODO explain
#------------------------------------------------------------------------------------------------------------------------------------------
def getPublicKeys(ssl_sock,networkSize):
    while networkSize != 0 :
        publickeys = ssl_sock.recv(1024)    #recieve public key of user from server
        if not publickeys:
            print("waiting for public keys")
            continue
        else:
            #print(publickeys.decode())     #debug
            networkSize = networkSize -1    #if the network size counter reaches zero all of the pubic keys have been recieved
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------
#get the public keys from the file TODO explain more
#------------------------------------------------------------------------------------------------------------------------------------------
def getPublicKey(user):
    public = ""
    public_file = open("public"+user+".pem", 'r')
    for line in public_file:
        public = public + line
    public_file.close()
    return public
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------
#genRSAKeyPairs #TODO inport this function from isaccs crypto class
#------------------------------------------------------------------------------------------------------------------------------------------
def genRSAKeyPairs(user):
    #Use OpenSSL to generate given bit modulus RSA keys NOT using Triple Data Encryption (-des3)
    subprocess.call(["openssl", "genrsa", "-out", "private" + user + ".pem", "2048"])

    #Write public key out to new file named publicX.pem
    subprocess.call(["openssl", "rsa", "-in", "private" + user + ".pem", "-outform", "PEM", "-pubout", "-out", "public" + user + ".pem"])
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------

def createSSLSocket():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Require a certificate from the server. We used a self-signed certificate
        # so here ca_certs must be the server certificate itself.
        ssl_sock = ssl.wrap_socket(s,
                                   ca_certs="mycert.pem",
                                   cert_reqs=ssl.CERT_REQUIRED)

        ssl_sock.connect(('localhost', 10000))
        return ssl_sock
#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------
#MAIN
#------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    networkSize = 2 #TODO make input at runtime

    ssl_sock  = createSSLSocket()        #create a ssl socket connection to server
    userid    = str(uuid.uuid4())        #generate a unique userid
    genRSAKeyPairs(userid)               #generate a public and private key for user
    publickey = getPublicKey(userid)     #get the publickey of the user from the file publickey<userid>.pem


    userinfo['id']        = userid
    userinfo['publickey'] = publickey

    ssl_sock.write (json.dumps(userinfo).encode()) #send the publickey and the user id to the server
    getPublicKeys  (ssl_sock  ,networkSize)       #get the public keys from all users in the network
    sendTransaction(ssl_sock  ,userid     )       #send a transation to another user

#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
