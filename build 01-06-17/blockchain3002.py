import json
import collections

#Karl Chen Gan
#Isaac R. Ward
#Creates a block from successful mining data
def makeBlock(blockchain, miningData):
    #Allows ordering data for the sake of relevance
    block = collections.OrderedDict()
    
    #Get the new block's height
    block['height'] = len(blockchain) + 1
    
    #Get the last block's hash, unless this is the first block
    if(len(blockchain) != 0):
        block['previous hash digest (as hex)'] = blockchain[len(blockchain) - 1]['hash digest (as hex)']
    else:
        block['previous hash digest (as hex)'] = "undefined"
    
    #Read in other details require by block in order
    block['hash digest (as hex)'] = miningData['metrics']['d']
    block['hash digest (as int)'] = int(miningData['metrics']['d'], 16)
    block['target at time mined'] = miningData['metrics']['target']
    block['seconds to mine'] = miningData['metrics']['t']
    block['nonce used'] = miningData['metrics']['n']
    block['transaction'] = miningData['transaction']
    block['miner'] = miningData['miner']
    
    return block

#Karl Chen Gan
#Isaac R. Ward
#Prints visual representation of the blockchain
def printBlockchain(blockchain):
    print("===========================[ START BLOCKCHAIN ]===========================")
    
    for b in blockchain:
        print("================================[ BLOCK " + str(b['height']) + " ]================================")
        print(json.dumps(b, indent = 4))
        
    print("============================[ END BLOCKCHAIN ]============================")

#Isaac R. Ward 
#Prints visual representation of the blockchain using file names rather than key strings when possible
def printBlockchainWithFileNames(blockchain, fileKeyPairs):
    print("===========================[ START BLOCKCHAIN ]===========================")
    
    for b in blockchain:
        print("================================[ BLOCK " + str(b['height']) + " ]================================")
        #If the printer has the miner's public key string saved as a file, print the file instead
        tmpMiner = b['miner']
        tmpSrc = b['transaction']['srcPubKey']
        tmpDest = b['transaction']['destPubKey']
        
        for p in fileKeyPairs:
            #Replace where miner public key is displayed in block
            if b['miner'] == p['string']:
                b['miner'] = p['file']
            
            #Replace where src & dest public keys are displayed in transactions with file names
            if b['transaction']['srcPubKey'] == p['string']:
                b['transaction']['srcPubKey'] = p['file']
                
            if b['transaction']['destPubKey'] == p['string']:
                b['transaction']['destPubKey'] = p['file']
        
        #Print with altered string
        print(json.dumps(b, indent = 4))
        
        #Put strings back
        b['miner'] = tmpMiner
        b['transaction']['srcPubKey'] = tmpSrc
        b['transaction']['destPubKey'] = tmpDest
        
    print("============================[ END BLOCKCHAIN ]============================")


