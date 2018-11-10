""""
Lydia Noureldin (12ln19) 
December 12 2017
CISC 435: Computer Networks
Server class for Proxy
"""

from socket import *
import socket
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from ClientInfo import ClientInfo
import datetime
import threading
import urllib
from urllib.request import urlopen
import ssl


class Server:

    def __init__(self):
        """
        Constructor for Server  
        """
        self.numActiveConnections = 0
        self.portNum = 9999  # arbitrary
        self.clients = {}  # dict of ClientInfo objects key is the IP address
        self.maxConnections = 3
        self.IP = socket.gethostbyname("")
        self.serverSocket = -1  # Placeholder
        self.setSocket()
        self.BUFFER_SIZE = 10000 # bytes


    def setSocket(self):
        # create a TCP/IP socket object
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind to the port
        self.serverSocket.bind((self.IP, self.portNum))

    def addClient(self, clientAddress):
        clientName = "client" + str(len(self.clients) + 1)#str(self.numActiveConnections + 1)
        self.clients[clientAddress] = ClientInfo(clientName) #"Platinum")  #add extra parameter here to test
        # Update number of active connections
        self.numActiveConnections = self.numActiveConnections + 1

    # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    def isValidURL(self, URL):
        # returns False / True boolean depending if the website follows https://www.----.com/ca/etc format
        # if you set verify_exists to True, it will actually verify that the URL exists,
        # otherwise it will just check if it's formed correctly.
        val = URLValidator()
        try:
            val(URL)
        except ValidationError:
            return False
        return True

    def listenForConnection(self):
        MAX_QUEUED_CONNECTIONS = 5
        # Listen for incoming connections
        self.serverSocket.listen(MAX_QUEUED_CONNECTIONS)
        while True:
            # Wait for a connection
            print("Waiting for connection...")
            clientSocket, clientAddress = self.serverSocket.accept()
            # Check to see if the server can make the connection
            if self.numActiveConnections < self.maxConnections:
                # Start a new thread to support concurrent connections
                threading.Thread(target=self.getClientRequests, args=(clientSocket, clientAddress)).start()
            else:
                clientSocket.sendall(
                    "Cannot connect to the server at this time - too many connections. Please try again later.".encode('utf-8'))
                clientSocket.close()

    def getClientRequests(self, clientSocket, clientAddress):
            print('Connected by: ', clientAddress)
            # Check if this is a new connection
            if clientAddress not in self.clients:
                self.addClient(clientAddress)
            try:
                # While client hasn't finished their quota
                while self.clients[clientAddress].remainingURLs > 0:
                    # Get the URL from the user
                    data = clientSocket.recv(self.BUFFER_SIZE)
                    # Get date and time that the request was received
                    requestDateTime = datetime.datetime.now()
                    stringData = data.decode("utf-8")
                    print('Client URL requested: ', stringData)
                    # if user is platinum and requests http://clientsusage.com return the other clients usage
                    # else check if the url is valid then update the client usage if they got it or not
                    urlValidityCheck = self.isValidURL(stringData)
                    if data:
                        self.getWebpage(urlValidityCheck, clientAddress, clientSocket, stringData, requestDateTime)
                    else:
                        print('No more data from ', clientAddress)
                        break
                # client finished their quota so close their socket and update number of active connections also
                # the server sends a response with this meaning
                clientSocket.sendall("You have reached your maximum number of URL requests. Terminating the connection.".encode('utf-8'))
                clientSocket.close()
            finally:
                # Clean up the connection
                print("Closing the connection.")
                clientSocket.close()
                self.numActiveConnections = self.numActiveConnections - 1

    def getWebpage(self, urlValidityCheck, clientAddress, clientSocket, stringData, requestDateTime):
        print("Letting the user know if their request was fulfilled")
        serverResponse = ""
        # if the URL the user is requesting is not in proper format ie. https://www.somewebsite.com
        if urlValidityCheck is False:
            self.clients[clientAddress].updateUsageDetails(stringData, requestDateTime.date(), requestDateTime.time(), False)
            serverResponse = serverResponse + "\nInvalid URL. Please try again."
        # URL was in proper format
        else:
            self.clients[clientAddress].updateUsageDetails(stringData, requestDateTime.date(), requestDateTime.time(), True)
            # Check if its the special webpage http://clientsusage.com for Platnum users
            if self.clients[clientAddress].category == "Platinum" and stringData == "http://clientsusage.com":
                clientUsageDetails = self.getClientUsageDetails()
                serverResponse = serverResponse + '\n' + clientUsageDetails
            # normal webpage
            else:
                serverResponse = serverResponse + "\nValid URL. Connecting to the webpage."
                htmlContents = self.getHTML(stringData)
                serverResponse = serverResponse + '\xff' + htmlContents
        clientSocket.sendall(serverResponse.encode('utf-8'))
        # Print statement for testing
        print(self.clients[clientAddress])

    def getHTML(self, URL):
        htmlContents = ""
        # get the html contents
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(URL, context=context) as response:
            html = response.read()
        htmlContents = html.decode("latin-1")
        return htmlContents

    def getClientUsageDetails(self):
        # For when Platnum users request  http://clientsusage.com
        output = ""
        for aClient in self.clients:
            output = output + "\n" + str(self.clients[aClient])
        return output

    def __str__(self):
        clientDetails = ""
        for aClient in self.clients:
            clientDetails = clientDetails + "\n" + str(self.clients[aClient])
        output = "\n\n~~Server Details~~ \nIP address: " + str(self.IP) + "\nPort Number: " + str(self.portNum) \
                 + "\nMaximum concurrent connections: " + str(self.maxConnections) + "\nNumber of current active connections: "  \
                 + str(self.numActiveConnections) + "\nClient details: " + clientDetails + "\n\n"
        return output
