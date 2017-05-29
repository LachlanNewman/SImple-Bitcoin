#Konrad Obara
# GUI interface for CITS3002 Project 2
from tkinter import *
from tkinter import messagebox

from crypto3002 import *
from blockchain3002 import *
from walletFunctions3002 import *
global master
global connect

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
	connect = Tk()
	connect.title("Server Connection")

	def establishConnection():
	#addy = addyEntry.get()
	#IF server does not exist
		messagebox.showerror("Server/Port error", "Server/Port does not exist")
		addyEntry.delete(0, 'end')
		portEntry.delete(0, 'end')
	#Else if ip is correnct
		#

	
	connect.geometry('300x300')
	addyLabel = Label(connect ,text = "Enter the Servers Local IP Address", font = "Impact 10 underline")
	portLabel = Label(connect, text = "Enter the Servers Port", font = "Impact 10 underline")
	addyEntry = Entry(connect, selectborderwidth = 50, width = 14) 
	portEntry = Entry(connect, selectborderwidth = 50, width = 4)
	addyButton = Button(connect, text = "Connect", font = "25", padx = 30, pady = 30, command = establishConnection)


	addyLabel.place(y = 50, x = 40)
	addyEntry.place(y = 75, x = 95)
	portLabel.place(y = 100, x = 80)
	portEntry.place(y = 125, x = 135)
	addyButton.place(y = 160, x = 85)
	
		
def clientMenu:
	cMenu = Tk()
	cMenu.title()


def initServer():
	server = Tk()
	server.title("EE")


def initClient():
	Cmaster = Tk()
	Cmaster.title("Client")
	Cmaster.geometry("750x600")


def initMiner():
	Mmaster = Tk()
	Mmaster.title("Miner")
	Mmaster.geometry("750x600")

def quit():
	global master
	master.quit()

initGUI()
