#Isaac R. Ward
#Run on linux with 'python3 testing.py'

from CryptographyFunctions import *

#Main code
if __name__ == '__main__':
    #In the wallet, generate info for two users and construct a message and send
    genRSAKeyPairs("A")
    genRSAKeyPairs("B")

    #Test a message that should be false
    m = buildTransactionDict("B", "A", "50")
    m['transaction'] = "5"
    verifyTransactionDict(m)

    #Test a message that should verify
    m = buildTransactionDict("B", "A", "100")
    verifyTransactionDict(m)
    
	#Integer that hash needs to be less than 
    target = 2**256	#(hard) 0 < target < 2**256 (easy)
    requiredTime = 0.2	    #Seconds
    numberPerBatch = 100     #Number of hashes required before recalculating target

    totaltime = 0.0
    amount = 0.0
	
    while(True):
    	timelog = []
    	
    	#In the miner, do proof of work algorithm on given message
    	for i in range(0, numberPerBatch - 1):
    		m = buildTransactionDict("B", "A", amount)
    		amount = amount + 1
    		count, timeTaken, nonce, hexDigest = proofOfWork(m, target)
    		print("Crypto hash cracked in " + str(count) + " hashes w/ nonce " + str(nonce) + " in time: " + str(timeTaken))
    		timelog.append(timeTaken)
    	
    	totaltime = sum(timelog)
    	target = int(target/(requiredTime*numberPerBatch/totaltime))
    	
    	print("Total time to crack hashes: " + str(totaltime))
    	print(str(requiredTime*numberPerBatch/totaltime)+ " times too easy, \nnew difficulty = " + str(target))


