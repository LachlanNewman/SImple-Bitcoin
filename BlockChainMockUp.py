#Isaac R. Ward
#Run on linux with 'python3 BlockChain.py'

from collections import namedtuple

Transaction = namedtuple("Transaction", "src dest amount nonce")
Block = namedtuple("Block", "transaction name prevName")

def printTransaction(t):
	print("|\t" + t[0] + " |-- $" + str(t[2]) + " --> " + t[1] + " with nonce: " + t[3])


def printBlock(b):
	print("\t/\\")
	print("\t||")
	print("\t||\n----------------------------------------------------------")
	print("|  Name           : " + b[1])
	print("|  Previous       : " + b[2])
	print("|  Transaction(s) :")
	printTransaction(b[0])
	print("----------------------------------------------------------")

#Main code
if __name__ == '__main__':

	t1 = Transaction("A", "B", 100, "HIJUROVOINCMUQPW")
	t2 = Transaction("B", "A", 50, "ASDDFMUQPFDSGFSW")
	t3 = Transaction("B", "A", 25, "RRRTERGBTYIUTEFD")
	t4 = Transaction("B", "A", 5, "TRWQQQHFIYOUGTER")

	
	b1 = Block(t1, "0001", "NULL") #Null as its the first block
	b2 = Block(t2, "ABCD", "0001")
	b3 = Block(t3, "QF9A", "ABCD")	
	b4 = Block(t4, "7YGT", "QF9A")

	BlockChain = []
	BlockChain.append(b1)
	BlockChain.append(b2)
	BlockChain.append(b3)
	BlockChain.append(b4)

	print("~~~~~~~~~~~~SAMPLE BLOCK CHAIN~~~~~~~~~~~~~~")

	for b in range(len(BlockChain)):
		printBlock(BlockChain[b])


	

