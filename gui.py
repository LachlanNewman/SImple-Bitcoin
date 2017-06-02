#Konrad Obara
# GUI interface for CITS3002 Project 2
from tkinter import *
from tkinter import messagebox
# server import *
#from crypto3002 import *
#from blockchain3002 import *
#from walletFunctions3002 import *
global master
global connect
global userEntry
global coinbase

def initGUI():
	global master
	master = Tk()
	master.title("CITS3002 Simple Bitcoin Emulator")
	master.geometry("750x250")
	#master.iconbitmap(r'/home/konrad/Desktop/GUI/coins.ico')
	TitleLabel = Label(master, text="CITS3002 Simple Bitcoin Emulator", font = "Impact 30 underline", fg = 'blue')
	CreatorLabel = Label(master, text="Created By: Konrad, Lanchan, Issac, Karl", font = "Impact")
	TitleLabel.pack()
	CreatorLabel.pack() 

	MainFrame = Frame(master, height = 250, width = 700)
	MainFrame.pack()

	server = Button(MainFrame, text="Server", fg="red", padx = 100, pady= 25, command = initServer)
	server.pack( side = LEFT)

	Miner = Button(MainFrame, text="Miner", fg="green", padx = 100, pady= 25, command = initMiner)
	Miner.pack( side = LEFT )

	client = Button(MainFrame, text="Wallet", fg="blue", padx = 100, pady= 25, command = connectServer)
	client.pack( side = LEFT )

	exit = Button(master, text="Exit", fg="black", padx = 100, pady= 25, command = quit )
	exit.pack( side = BOTTOM )


	master.mainloop()

def connectServer():
	global master
	global connect
	global userEntry
	connect = Tk()
	connect.title("Server Connection")

	def establishConnection():

	#addy = addyEntry.get()
	#IF server does not exist
		messagebox.showerror("Server/Port error", "Server/Port does not exist")
		addyEntry.delete(0, 'end')
		portEntry.delete(0, 'end')
		clientMenu()
	#Else if ip is correnct
		

	def clientMenu():

		def sendTrans():
			function

		def checkBalance():
			#global coinbase
			#userBalance = checkBalance(blockchain, uname, coinbase)
			messagebox.showinfo("Balance", "Your Balance equals %d" % userBalance)

		def checkUsersBalanceFunc():
			TheirUserName = checkUsersBalanceLabel.get()
			TheirBalance = checkBalance(TheirUserName)
			messagebox.showinfo("Balance", "Your Balance equals %d" % MyBalance)

		cMenu = Tk()
		cMenu.title("Client Menu")
		cMenu.geometry("500x420")
		uname = userEntry.get()
		userName = Label(cMenu, text = uname, font = "Impact 25 underline" )

		amonutLabel = Label(cMenu, text = "Enter Amount", font = "Impact 10 underline")
		amount = Entry (cMenu, selectborderwidth = 50, width = 12)

		recipientLabel = Label(cMenu, text = "Enter recipient's username", font = "Impact 10 underline")
		recipient = Entry(cMenu, selectborderwidth = 50)

		send = Button(cMenu, text = "Send Transaction",font = "25", padx = 30, pady = 30, command = sendTrans)

		balance = Button(cMenu, text = "Check your balance", font = "25", padx = 30, pady = 30, command = checkBalance)

		checkUsersBalanceLabel = Label(cMenu, text = "Enter Users Username", font = "Impact 10 underline") 
		checkUsersBalance = Entry(cMenu, selectborderwidth = 50)
		checkUsersBalanceButton = Button(cMenu, text = "Check", padx = 30, pady= 15, command = checkUsersBalanceFunc)

		userName.place(y = 30, x = 150)
		amonutLabel.place(y= 170, x= 25)
		amount.place(y = 200, x = 25)
		recipientLabel.place( y = 230, x = 25)
		recipient.place( y = 260, x = 25)
		send.place(y = 295, x = 25)
		balance.place(y = 295, x = 260)
		checkUsersBalanceLabel.place(y = 170, x= 260)
		checkUsersBalance.place(y = 200, x = 260)
		checkUsersBalanceButton.place(y = 230, x = 285)




	
	connect.geometry('300x300')
	addyLabel = Label(connect ,text = "Enter the Servers Local IP Address", font = "Impact 10 underline")
	passLabel = Label(connect ,text = "Enter your private key", font = "Impact 10 underline")
	portLabel = Label(connect, text = "Enter the Servers Port", font = "Impact 10 underline")
	userLabel = Label(connect, text = "Enter your local key", font = "Impact 10 underline")
	passEntry = Entry(connect, selectborderwidth = 50)
	addyEntry = Entry(connect, selectborderwidth = 50, width = 14) 
	portEntry = Entry(connect, selectborderwidth = 50, width = 4)
	userEntry = Entry(connect, selectborderwidth = 50)
	addyButton = Button(connect, text = "Connect", font = "25", padx = 30, pady = 30, command = establishConnection)


	
	userLabel.place(y = 5, x = 90)
	userEntry.place(y = 25, x = 70)
	passLabel.place(y = 50, x = 80)
	passEntry.place(y = 75, x = 70)
	addyLabel.place(y = 100, x = 40)
	addyEntry.place(y = 125, x = 95)
	portLabel.place(y = 155, x = 80)
	portEntry.place(y = 175, x = 135)
	addyButton.place(y = 200, x = 85)

	
		




def initServer():
	server = Tk()
	server.title("Server")
	server.geometry('300x300')
	
	serverLabel = Label(server, text = "Input the port you want to use", font = "Impact 10 underline")
	serverEntry = Entry(server, selectborderwidth = 50)

	timeLabel = Label(server, text = "Time it takes to mine 1 transacion", font = "Impact 10 underline")
	timeEntry = Entry(server, selectborderwidth = 50)

	sucessLabel = Label(server, text =  "Batch size", font = "Impact 10 underline")
	sucessEntry = Entry(server, selectborderwidth = 50)

	serverButton = Button(server, text = "Create Server", font = "25", padx = 30, pady = 30)

	serverLabel.place(y = 10, x = 60)
	serverEntry.place(y = 35, x = 70)
	timeLabel.place(y = 55, x = 40)
	timeEntry.place(y = 80, x = 70)
	sucessLabel.place(y = 105, x = 115)
	sucessEntry.place(y = 130, x = 70)
	serverButton.place(y = 170, x = 70)



def initClient():
	Cmaster = Tk()
	Cmaster.title("Client")
	Cmaster.geometry("750x600")


def initMiner():
	Mmaster = Tk()
	Mmaster.title("Miner")
	
	def startMiner():
		minerWindow = Tk()
		minerWindow.title("Miner Interface")
		minerWindow.geometry('300x430')

		def mineTrans():
			messagebox.showinfo("Sucessfully Mined", "You sucessfully mined the transaction and received 50 units")

		TransLabel = Label(minerWindow, text = "List of unmined transacions", font = "Impact 12 underline")
		TransList = Listbox(minerWindow, bd = 8, font = "Impact 12 ", width = 5)
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		TransList.insert(1, "1")
		MineThis = Label(minerWindow, text = "Input transaction you want to mine", font = "Impact 10 underline")
		MineInput = Entry(minerWindow, selectborderwidth = 50 , width = 1)
		MineThisButton = Button(minerWindow, text = "Mine", padx = 50, pady= 15, command = mineTrans)
		TransLabel.place(x = 45, y = 30)
		TransList.place(x = 120, y = 55)
		MineThis.place(x = 40, y = 300)
		MineInput.place(x = 145, y =330)
		MineThisButton.place(x = 85, y = 360)


	Mmaster.geometry('300x300')
	addyLabel = Label(Mmaster ,text = "Enter the Servers Local IP Address", font = "Impact 10 underline")
	
	portLabel = Label(Mmaster, text = "Enter the Servers Port", font = "Impact 10 underline")
	userLabel = Label(Mmaster, text = "Enter your user ID", font = "Impact 10 underline")
	
	addyEntry = Entry(Mmaster, selectborderwidth = 50, width = 14) 
	portEntry = Entry(Mmaster, selectborderwidth = 50, width = 4)
	userEntry = Entry(Mmaster, selectborderwidth = 50)
	addyButton = Button(Mmaster, text = "Connect", font = "25", padx = 30, pady = 30, command = startMiner)


	
	userLabel.place(y = 10, x = 90)
	userEntry.place(y = 30, x = 70)
	
	addyLabel.place(y = 55, x = 40)
	addyEntry.place(y = 80, x = 95)
	portLabel.place(y = 105, x = 80)
	portEntry.place(y = 130, x = 135)
	addyButton.place(y = 170, x = 85)

def quit():
	global master
	master.quit()

initGUI()
