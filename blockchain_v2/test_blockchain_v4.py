#!/user/bin/python3

import blockchain_v4

#initial block
blockchain_v4.firstblock()

#add new block to blockchain
blockchain_v4.newblock()

#get first block
print(blockchain_v4.blockchain[0])

#get 2nd block
print(blockchain_v4.blockchain[1])
