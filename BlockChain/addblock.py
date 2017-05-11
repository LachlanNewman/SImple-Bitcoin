#Karl CHEN 10.5.2017

#!/usr/bin/python3

#receiving data including blockinfo(this block id, prev block id, nonce)
#and transactioninfo(amount of coin, from someone, to someone) )

#datacoin, datafrom, datato
#datablockid, dataprevid, datanonce

import blockclass

#create a list including transaction info
t = block.trans(datacoin, datafrom, datato)
ti = t.createtrans()

#create a list including block info and transaction info
b = block.block(datablockid, dataprevid, datanonce, ti)
#count the height and create a "block"
bi = b.createblock()
b.addblock()


#to do
#initialise first block
#check transaction history
#get block infomation
