


class Wallet(object):

    def __init__(self):
        self.wallet = [] #list to hold all trasactions
        print("wallet initialised")

    def intial_transactions(self,user):
        #TODO send random transaction with amout zero from one user to another
        #who ever mine this trasactionrecieves some amount of money
        #dictionay  values sender - takes from amount
        # reciever add to amount
        # if it mined sender is pre defined value -> mined and ingored

        # test transacion
        print("users = " + user)
        transaction = {}
        transaction['destID'] = user
        transaction['srcID'] = 'Bank'
        transaction['Amount'] = 50
        self.wallet.append(transaction)
        print(self.wallet)
