from tkinter import *
from crypto3002 import *
from blockchain3002 import *
from walletFunctions3002 import *


def initGUI():
	master = Tk()
	master.title("CITS3002 Simple Bitcoin Emulator")
	master.geometry("750x250")

	TitleLabel = Label(master, text="CITS3002 Simple Bitcoin Emulator", font = "Impact 30 underline", fg = 'blue')
	CreatorLabel = Label(master, text="Created By: Konrad, Lanchan, Issac, Karl")
	TitleLabel.pack()
	CreatorLabel.pack() 

	MainFrame = Frame(master, height = 250, width = 700)
	MainFrame.pack()

	server = Button(MainFrame, text="Server", fg="red", padx = 100, pady= 25, command = initServer)
	server.pack( side = LEFT)

	Miner = Button(MainFrame, text="Miner", fg="brown", padx = 100, pady= 25, command = initMiner)
	Miner.pack( side = LEFT )

	client = Button(MainFrame, text="Wallet", fg="blue", padx = 100, pady= 25, command = initClient)
	client.pack( side = LEFT )

	exit = Button(MainFrame, text="Exit", fg="black", padx = 100, pady= 25)
	exit.pack( side = BOTTOM )


	master.mainloop()

def initServer():
	Smaster = Tk()
	Smaster.title("Server")
	Smaster.geometry("750x600")



def initClient():
	Cmaster = Tk()
	Cmaster.title("Client")
	Cmaster.geometry("750x600")


def initMiner():
	Mmaster = Tk()
	Mmaster.title("Miner")
	Mmaster.geometry("750x600")



initGUI()
