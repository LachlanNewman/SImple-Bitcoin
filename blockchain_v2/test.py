#Karl CHEN 15.5.2017

import blockclass_v2

#create the first block
blockclass_v2.firstblock()

#create transaction dict with transaction detail
t = blockclass_v2.trans(100,'alice','bob','sdfe3r43r34r')
ti = t.createtrans()

#create block dict with block detail
b=blockclass_v2.block('2342','123101',ti)
bi = b.createblock()

#add block to block chain
b.addblock()

#get block info by the height
b.getblockinfo()
b.getblockinfo()
