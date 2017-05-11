import blockclass

t = blockclass.trans(100,'a','b')
ti = t.createtrans()
b=blockclass.block(333,222,123101,ti)
bi = b.createblock()
b.addblock()
