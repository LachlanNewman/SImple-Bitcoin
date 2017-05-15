### blockclass_v2 test instruction</br>
blockclass_v2 stores block in .db file instead of .txt
```
blockclass_v2.firstblock() 
```
will create a .db file with the info of first block, you'll need to type in the amount of coins and the account who receive it</br></br>

```
t = blockclass_v2.trans(100,'alice','bob')
ti = t.createtrans()
```
will create a transaction dict with transaction detail</br></br>

```
b=blockclass_v2.block('2342',123101,ti)
bi = b.createblock()
```
create a block dict with block detail</br></br>

```
b.addblock()
```
add/store the block in blockchain.db</br></br>

```
b.getblockinfo()
```
get info of a block by specifying the height
