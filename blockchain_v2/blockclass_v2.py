#Karl CHEN 15.5.2017

#!/usr/bin/python3

import shelve

class trans:
    amount = 0
    addressfrom = ''
    addressto = ''
    signature = ''

    def __init__(self, am, adf, adt, sign):
        self.amount = am
        self.addressfrom = adf
        self.addressto = adt
        self.signature = sign

    #transaction details
    def createtrans(self):
        transinfo = {
            'transaction from':self.addressfrom,
            'transaction to':self.addressto,
            'amount':self.amount,
            'digital signature':self.signature
            }
        return transinfo


#initialise first block
def firstblock():
    owner = input('who wants money: ')
    firstcoin = input('how much do you want: ')
    fb = shelve.open('blockchain')
    fb.update({"1":{'height':'1',
                    'block information':{'block id':'cits3002',
                                        'prev block id':'',
                                        'nonce':''},
                    'transaction information':{'transaction from':'CHEN Gan',
                                              'transaction to':owner,
                                              'amount':int(firstcoin)}}})
    fb.close()


class block(trans):
    blockid = 0
    nonce = 0
    detail = {}
    height = 0
    
    def __init__(self, bid, non, transinfo):
        self.blockid = bid
        self.nonce = non
        self.detail = transinfo

    #block details
    def createblock(self):
        #count the height of blockchain
        counth = shelve.open('blockchain')
        #the height of new block
        height = len(counth) + 1
        #get the id of previous block
        getid = shelve.open('blockchain')
        previd = getid[str(height - 1)]['block information']['block id']
        getid.close()
        
        #info of a block
        blockinfo = {
            'block id':self.blockid,
            'prev block id':previd,
            'nonce':self.nonce
            }
        
        #detail of a block including block info and transaction info
        blockdetail = {
            'height':str(height),
            'block information':blockinfo,
            'transaction information':self.detail
            }
        return blockdetail

    #add block to "blockchain.db"
    def addblock(self):
        bc = shelve.open('blockchain')
        height = len(bc) + 1
        bc.update({str(height):self.createblock()})
        bc.close()

    #get infomation of a block specified by height
    def getblockinfo(self):
        gb = shelve.open('blockchain')
        which = input('which block do you want: ')
        block_info = gb[which]
        gb.close()
        print(block_info)

