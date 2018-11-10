""""
Lydia Noureldin (12ln19) 
December 12 2017
CISC 435: Computer Networks
Server class for Proxy
"""

import socket
import webbrowser
import os


class Client:

    def __init__(self, serverAddress):
        self.IP = socket.gethostbyname("")
        self.portNum = 0
        self.clientSocket = -1
        self.setSocket(serverAddress)
        self.shutdown = False
        self.BUFFER_SIZE = 1024  # bytes

    def setSocket(self, serverAddress):
        # serverAddress is a tuple of type (string, int) ie. ('127.0.0.1', 5000)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Request connection to server
        print("Requesting connection to ", str(serverAddress))
        self.clientSocket.connect(serverAddress)

    def sendMessages(self):
        try:
            # Ask the user what URL they want to request
            clientInput = input("Please input URL or 'q' to quit: ")
            while clientInput != 'q' and clientInput != 'quit':
                if clientInput != '':
                    print("\n\nSending the message: ", clientInput)
                    self.clientSocket.sendall(clientInput.encode('utf-8'))
                    # look for response
                    data = self.myreceive()
                    stringData = data.decode('utf-8')
                    consoleMessage, htmlContents = self.separateMessage(stringData)
                    print('Message from the server: ', consoleMessage)
                    # If data says server disconnected then closes its connection here to
                    # free resources for other clients
                    if consoleMessage == "You have reached your maximum number of URL requests. Terminating the connection." or \
                        consoleMessage == "Cannot connect to the server at this time - too many connections. Please try again later.":
                        break
                    elif htmlContents != "":
                        self.openWebpage(htmlContents)
                clientInput = input("Please input URL or 'q' to quit: ")
            self.shutdown = True
        finally:
            print("Closing client socket")
            self.clientSocket.close()


    # https://docs.python.org/3.4/howto/sockets.html
    # equivalent to recvall that for some reason doesn't exist in the Python library
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd <= self.BUFFER_SIZE:
            chunk = self.clientSocket.recv(self.BUFFER_SIZE)
            if chunk == b'':
                print("Socket connection broken")
            chunks.append(chunk)
            bytes_recd = len(chunk)
            if bytes_recd < self.BUFFER_SIZE:
                break
        return b''.join(chunks)

    # Separates the text to be printed to the console from the html file
    def separateMessage(self, data):
        consoleMessage = ""
        htmlContents = ""
        htmlStart = 0
        for i in range(len(data)):
            if data[i] != '\xff':
                consoleMessage = consoleMessage + data[i]
                htmlStart = htmlStart + 1
            else:
                break
        if htmlStart > len(data) - 1:
            htmlContents = ""
        elif data[htmlStart] == '\xff':
            # i + 1 to get rid of null char
            htmlContents = data[htmlStart+1:]
        return consoleMessage, htmlContents

    def openWebpage(self, htmlContents):
        htmlFilePath = os.path.realpath("urlContents.html")
        if os.path.exists(htmlFilePath) is True:
            os.remove(htmlFilePath)
        fh = open("urlContents.html", "w")
        fh.write(htmlContents)
        fh.close()
        webbrowser.open('file://' + os.path.realpath("urlContents.html"))


