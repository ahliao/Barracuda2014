import socket
import json
import struct
import time
import sys
import math

import Comm
import cardCount

class Player:
	def __init__(self):
		self.counter = cardCount.CardCount()
		self.lastPlayed = None

	def playRequest(self, comm):
		if comm.player_num == 1:
			self.counter.updateDeck(comm.card)

		playCard = 0
		comm.hand.sort()
		if (comm.card == None):
			playCard = comm.hand[int(math.floor(len(comm.hand) / 2))]
		else:
			for card in comm.hand:
				if card > comm.card:
					playCard = card
					break

		lastPlayed = playCard
		comm.playCard(playCard)
		self.counter.updateDeck(playCard)

		
	def challenged(self, comm):
		comm.acceptChallenge()

	def result(self, comm):
		if comm.player_num == 0 and (comm.resultType == "trick_won" or comm.resultType == "trick_tied"):
			self.counter.updateDeck(comm.card)