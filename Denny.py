import socket
import json
import struct
import time
import sys

import Comm
class Player:
	def __init__(self):
		self.cardCount[8,8,8,8,8,8,8,8,8,8,8,8,8]
		self.expectedValue
		self.turn #who started me or not me
		
	def playRequest(self, comm):
		if comm.card == None:
			turn = "me"
		else:
			turn = "not me"
			cardCount[comm.card--]--
		
		comm.playCard(comm.hand[0])
		# comm.sendChallenge()
		
	def challenged(self, comm): #if I am challenged I will check my expected value of the cards in my hand and see to accept.
		evalue = calcvalue(comm)
		comm.acceptChallenge()
		comm.rejectChallenge()
		
	def result(self, comm):
		if turn == "me":
			cardCount[comm.card--]--
			
	def calcvalue(self, comm):
		value = 0
		value += comm.your_tricks * 0.2
		size = len(comm.hand)
		sum = 0
		above = 0
		for i in xrange(0,13):
			sum += cardCount[i]
		#sum calculated
		for x in range(0,size):
			for y in range(0,comm.hand[x] - 1):
				above += cardCount[y]
		return float(above)/sum
			
		
	

