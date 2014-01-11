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
		# print("cardNum: " + str(cardNum))
		if (cardNum != None):
			self.deck[cardNum - 1] -= 1
			self.numCards -= 1

	def getAvg(self):
		total = 0
		for i in range(0, 13):
			total += (i + 1) * self.deck[i]
		numCards = 0
		for cards in self.deck:
			numCards += cards

		if (numCards == 0):
			numCards = 1
		return total / numCards
