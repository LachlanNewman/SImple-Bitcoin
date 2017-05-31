#Konrad Obara
#Checks and returns the balance of a user on the network by looking through a given blockchain
def checkBalance(blockchain, publicKey, coinbase):
    #The starting balance of user with given public key
    balance = 0
    
    for b in blockchain:
        if b['transaction']['destPubKey'] == publicKey:
            #If the person is the receiver, they should gain that money
            balance += int(b['transaction']['amount'])
            
        elif b['transaction']['srcPubKey'] == publicKey:
            #If the person is the sender, they should lose that money
            balance -= int(b['transaction']['amount'])
            
        if b['miner'] == publicKey:
            #If the person is the miner of the block, they should gain the 'coinbase'
            balance += coinbase
            
    return balance

