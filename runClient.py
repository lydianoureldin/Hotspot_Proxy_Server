""""
Lydia Noureldin (12ln19) 
December 12 2017
CISC 435: Computer Networks
Server class for Proxy
"""

from Client import Client

def main():
    serverTuple = ('0.0.0.0', 9999)
    client1 = Client(serverTuple)
    client1.sendMessages()

main()

