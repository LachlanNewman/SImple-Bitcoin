#Karl CHEN, 22/05/2017
#!/user/bin/python3

import json

blockchain = []
#print(blockchain)

def firstblock():
    #get transaction detail from .json
    transaction = open('trans.json')
    transdetail = json.load(transaction)
    transaction.close()
    #initial the previous hash of first block with 256 zeros
    first_prevhash = '0'*256
    #put details into dict
    first_block = {}
    first_block['height'] = '1'
    first_block['sender'] = transdetail['Sender']
    first_block['receiver'] = transdetail['Recipient']
    first_block['transaction'] = transdetail['Amount']
    first_block['signature'] = transdetail['Signature']
    first_block['hash'] = 'blockhash'#from crypto function
    first_block['previous_hash'] = first_prevhash
    first_block['nonce'] = 'nonce'#from crypto function
    #append first block to block chain
    blockchain.append(first_block)
    #print(blockchain)
    return blockchain

def newblock():
    #get transaction detail from .json
    transaction = open('trans.json')
    transdetail = json.load(transaction)
    transaction.close()

    #get the number of new block
    height = len(blockchain) + 1
    #get the hash of previous block
    prev_hash = blockchain[height - 2]['hash']

    #put details into dict
    new_block = {}
    new_block['height'] = height
    new_block['sender'] = transdetail['Sender']
    new_block['receiver'] = transdetail['Recipient']
    new_block['transaction'] = transdetail['Amount']
    new_block['signature'] = transdetail['Signature']
    new_block['hash'] = 'blockhash'#from crypto function
    new_block['previous_hash'] = prev_hash
    new_block['nonce'] = 'nonce'#from crypto function
    blockchain.append(new_block)
    #print(blockchain)
    return blockchain

'''
def dump()
    for b in blockchain:
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
'''
