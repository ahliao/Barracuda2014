import socket
import json
import struct
import time
import sys

class CardCount:
    def __init__(self):
        self.deck = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
        self.numCards = 8 * 13

    def refreshDeck(self):
        self.deck = [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
        self.numCards = 8 * 13

    def updateDeck(self, cardNum):
    	print("cardNum: " + str(cardNum))
    	if (cardNum != None):
	    	self.deck[cardNum - 1] = self.deck[cardNum - 1] - 1
    		self.numCards -= 1

    def getAvg(self):
    	total = 0
    	for card in self.deck:
    		total += card
    	return total / self.numCards
	