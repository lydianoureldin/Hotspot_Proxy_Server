"""""
Lydia Noureldin (12ln19) 
December 12 2017
CISC 435: Computer Networks
ClientInfo class for Proxy
"""

import socket
import random
import math


class ClientInfo:

    def __init__(self, clientName, testingCategory=""):
        self.IP = socket.gethostbyname("")
        self.name = clientName
        self.accessCode = -1
        self.setAccessCode()
        self.category = ""
        # For testing, default will work normally
        if testingCategory != "":
            self.category = testingCategory
        else:
            self.setCategory()
        self.maxURLs = -1
        self.setMaxURLs()
        self.remainingURLs = self.maxURLs
        self.usageDetails = {}
        self.portNum = 0

    def setAccessCode(self):
        # Get a random integer from 50-300
        randAccessCode = random.randint(50, 300)
        self.accessCode = randAccessCode

    def setCategory(self):
        accessCodeStr = str(self.accessCode)
        lastDigit = int(accessCodeStr[-1])
        if lastDigit == 0:
            self.category = "Platinum"
        elif lastDigit % 2 == 0:
            self.category = "Silver"
        else:
            self.category = "Gold"

    def setMaxURLs(self):
        if self.category == "Platinum":
            self.maxURLs = math.inf
        elif self.category == "Gold":
            self.maxURLs = 5
        else:  # Silver
            self.maxURLs = 3

    def updateUsageDetails(self, URL, date, time, requestFulfilled):
        self.usageDetails[URL] = [str(date), str(time), requestFulfilled]
        if requestFulfilled is True:
            self.remainingURLs = self.remainingURLs - 1

    def __str__(self):
        usageDetailsString = ""
        i = 1
        for key in self.usageDetails:
            usageDetailsString = usageDetailsString + "\n\tURL #" + str(i) + ": " + str(key) + "\n\tDate: " + str(self.usageDetails[key][0]) \
                                    + "\n\tTime: " + str(self.usageDetails[key][1])
            i = i + 1
        outputStr = "\n~~Client Information~~ \nName: " + self.name + "\nIP: " + str(self.IP) + "\nPort Number: " + str(self.portNum) \
                    + "\nAccess Code: " + str(self.accessCode) + "\nCategory: " + self.category + "\nMaximum URLs: " \
                    + str(self.maxURLs) + "\nURLs left: " + str(self.remainingURLs) + "\nUsage details: " + usageDetailsString+ "\n"
        return outputStr
