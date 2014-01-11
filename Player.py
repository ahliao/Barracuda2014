import socket
import json
import struct
import time
import sys

import Comm

class Player:
	def __init__(self):
		pass

	def playRequest(self, comm):
		if comm.card == None: # we go first
			if len(comm.hand) == 5:
				comm.playCard(comm.hand[2])
			else:
				comm.playCard(comm.hand[0])
		else:
			if comm.card >= max(comm.hand):
				# play the lowest card
				comm.playCard(comm.hand[len(comm.hand)-1])
			else:
				# play the lowest card that can win
				for x in reversed(range(len(comm.hand))):
					if comm.hand[x] > comm.card:
						comm.playCard(comm.hand[x])
				
		
	def challenged(self, comm):

		comm.acceptChallenge()

	def result(self, comm):
		pass
		
	

