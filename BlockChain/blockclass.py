#Karl CHEN 10.5.2017

#!/usr/bin/python3

class trans:
    amount = 0
    addressfrom = ''
    addressto = ''

    def __init__(self, am, adf, adt):
        self.amount = am
        self.addressfrom = adf
        self.addressto = adt

    #transaction details
    def createtrans(self):
        transinfo = [self.addressfrom, self.addressto, self.amount]
        return transinfo

class block(trans):
    blockid = 0
    previd = 0
    nonce = 0
    detail = []
    height = 0
    
    def __init__(self, bid, pid, non, transinfo):
        self.blockid = bid
        self.previd = pid
        self.nonce = non
        self.detail = transinfo

    #block details
    def createblock(self):
        #count the height of blockchain
        counth = open('blockchain.txt','r')
        nlines = len(counth.readlines())
        height= int((nlines // 2) + 1)
        
        #info of a new block
        blockinfo = [height, self.blockid, self.previd, self.nonce]
        #detail of a new block including block info and transaction info
        blockdetail = [blockinfo, self.detail]
        return blockdetail

    #add block to "blockchain"
    def addblock(self):
        bc = open('blockchain.txt','a')
        bc.write(str(self.createblock()))
        bc.write('\n\n')
        bc.close()


