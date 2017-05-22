import json
import os.path
import random
import uuid

global transList



def initTransList():
    global transList
    transList = []

# Open a wallet file on client restart ("Important Laters")
def openTransList():
    jpath = (os.path.dirname(__file__), 'wallet.json')
    walletPath = '/'.join(jpath)
    if os.path.isfile(walletPath):
        with open("%s" %walletPath) as loadedWallet:
            return json.load(loadedWallet)

# Appends a verified incoming message from the blockchain onto the wallet 
def appendTrans(msgFile):
    global transList
    jpath = (os.path.dirname(__file__), '%s.json' %msgFile)
    walletPath = '/'.join(jpath)
    with open('%s'%walletPath) as currTrans:
        tempMessage = json.load(currTrans)
        print(tempMessage)
    for trans in transList:
        if trans['Signature'] == sig:
            print('This transaction allready exists')
        else:                             
            transList.append(tempMessage)
    return transList
    
#Together with giveFunds appends transactions that send money to the users.
#Not a real transaction 

def giveFunds(users):
    global transList
    for user in users:
        randDict = {}
        randDict['destID'] = '%s' %user
        randDict['srcID'] = 'Bank'
        randDict['Amount'] = 50
        transList.append(randDict)
    print (transList)

# Checks and returns the balance of the currenty open wallet
def checkBalance(userID):
    balance = 0
    for trans in transList:
        if  trans['destID'] == userID:
            balance -= trans['Amount']
        elif trans['srcID'] == userID :
            balance += trans['Amount']
    return balance

def validTrans():
    jpath = (os.path.dirname(__file__), 'signedMessage.json')
    walletPath = '/'.join(jpath)
    with open('%s'%walletPath) as currTrans:
        tempMessage = json.load(currTrans)
    if tempMessage['Transaction'] <= checkBalance(tempMessage['srcID']):
        return True
    else:
        return False

# Saves the constructed wallet into a JSON file. Saves the wallet for each user. 
def applyToJson():
    global transList
    with open('%s' %walletPath,'w+') as loadedWallet:
        json.dump(transList, loadedWallet,indent= 4)
        
initTransList()
giveFunds(['A','B','C'])
validTrans()
