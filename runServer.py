""""
Lydia Noureldin (12ln19) 
December 12 2017
CISC 435: Computer Networks
Server class for Proxy
"""

from Server import Server

def main() :
    centralServer = Server()
    print(centralServer)
    centralServer.listenForConnection()

main()
