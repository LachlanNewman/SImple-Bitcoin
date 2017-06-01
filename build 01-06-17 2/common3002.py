import os.path, socket, ssl

#Isaac R. Ward
#Returns a list of pairings between actual public keys and the names of the files they are in
def getPublicPairs():
    pairList = []

    #Announce to user
    print("Reading .pem public key files from public keys directory:")
    found = False
    
    #Find all files in that directory
    for pkfile in os.listdir("publicKeys"):
        #If they are .pem files
        if pkfile.endswith(".pem"):
            found = True
            print("\tLoading " + str(pkfile))
        
            pair = {}
            
            #Get the filename
            pair['file'] = pkfile
            
            #Get the public key as a string
            pkString = ""
            for line in open("publicKeys/" + pkfile, 'r'):
                pkString = pkString + line
            pair['string']  = pkString
            
            #Add them to the given list
            pairList.append(pair)
            
    #Announce if no files were found
    if not found:
        print("\tNone found.")
            
    print("")

    return pairList

#Lachlan Newman
#Creates and returns an SSL socket
def createSSLSocket():
    #Generate a stream style socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Require a certificate from the server. We used a self-signed certificate
    #so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,
                               ca_certs="mycert.pem",
                               cert_reqs=ssl.CERT_REQUIRED)
                               
    #Get IP address from user
    IP = input("Enter server's IP address (localhost if server running on current machine):\n")
    
    #Get port number of server as user input and connect
    port = input("Enter server's port number:\n")
    ssl_sock.connect((IP, int(port)))
    
    return ssl_sock
    
