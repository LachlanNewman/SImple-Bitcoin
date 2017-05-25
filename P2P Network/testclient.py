import socket, ssl, pprint, uuid, subprocess, json, threading
from crypto import *

#TODO make headers in messages to differentiate between
#       -publickeys
#       -transactions
#       -mining signalsfor conn in clientConnections:
#       others??

target = 2**256

def recvTransaction(ssl_sock, userid,publickeys):
    print("\t\t\t\t\t\t\t transaction recieved")
    while True:
        data = json.loads(ssl_sock.recv(4096).decode())
        if not data:
            break
        #data = verifyTransactionDict(data) TODO issac  needs to fix verification
        #print(data)
        count, time, nonce, digest = proofOfWork(data,target)
        print("time: " + str(time) + ", nonce: " + str(nonce))

#------------------------------------------------------------------------------------------------------------------------------------------
#sends all transactions to server TODO EXPLAIN MORE
#------------------------------------------------------------------------------------------------------------------------------------------
def sendTransaction(ssl_sock,userid,publickeys):
    while True:
        print(userid + " make a transaction")
        dest       = input("id:"       )       #user id of reciever
        amount     = input("amount:"   )       #amount to transfer
        #comment']    = input("comment:"  )       #comment to go with transaction
        if dest =="X" and amount == "X":
            #condition to end socket connection TODO add to readme file
            break;
        transaction = buildTransactionDict(userid,dest,amount,publickeys)
        ssl_sock.send(json.dumps(transaction).encode())        #send transaction to server

#------------------------------------------------------------------------------------------------------------------------------------------
#get all the publickeys of users in the network #TODO explain
#------------------------------------------------------------------------------------------------------------------------------------------
def getPublicKeys(ssl_sock,networkSize,pbkeys):
    while networkSize != 0 :
        publickeys = json.loads(ssl_sock.recv(1024).decode())    #recieve public key of user from server
        if not publickeys:
            print("waiting for public keys")
            continue
        else:
            pbkeys[publickeys['id']] = publickeys['publickey']
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
        port = input("enter port number")
        # Require a certificate from the server. We used a self-signed certificate
        # so here ca_certs must be the server certificate itself.
        ssl_sock = ssl.wrap_socket(s,
                                   ca_certs="mycert.pem",
                                   cert_reqs=ssl.CERT_REQUIRED)

        ssl_sock.connect(('localhost', int(port)))
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

    publickeyinfo              = {}
    publickeyinfo['id']        = userid
    publickeyinfo['publickey'] = publickey
    publickeyinfo['header']    = 'publickey'
    publickeys = {}

    ssl_sock.write (json.dumps(publickeyinfo).encode()) #send the publickey and the user id to the server
    getPublicKeys  (ssl_sock  ,networkSize, publickeys)       #get the public keys from all users in the network
    print(publickeys)
    with open("publickeys.json","w") as fp:
        json.dump(publickeys, fp, indent=4)
    fp.close()
    sendTransaction = threading.Thread(target=sendTransaction, args=(ssl_sock,userid,publickeys))       #send a transation to another user
    recvTransaction = threading.Thread(target=recvTransaction, args=(ssl_sock,userid,publickeys))       #send a transation to another user
    sendTransaction.start()
    recvTransaction.start()

#------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------
