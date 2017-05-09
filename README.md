# CITS3002 - Simple Bitcoin Project

### Peer-to-Peer Network Instructions
Pull the latest commit and navigate to the directory P2P Network

run 

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem
```
#enter details when prompted

#run in a seperate shell for each users
```
python3 user.py
```

#after starting all users type RUN GETUSERS into each shell to connect the user to peers


### COMMANDS

#RUN GETUSERS => Connects user to peers in network

#ENDCONN      => Ends connection with user to peers


### TODO
all user (servers) will have to log the server there are running on into an online database for now type all the ports that the different users are running on into the text file csp.txt like so
````
8000
8001
8002
````
