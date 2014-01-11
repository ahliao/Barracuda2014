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
		self.opponent_cards = []

	def playRequest(self, comm):
		if comm.player_num == 1:
			self.counter.updateDeck(comm.card)
			self.opponent_cards.append(comm.card)

		if comm.can_challenge and self.calc_challenge(comm) > 3:
			comm.sendChallenge()
			return

		playCard = 0
		comm.hand.sort()
		if (comm.card == None):
			playCard = comm.hand[int(math.floor(len(comm.hand) / 2))]
		else:
			for card in comm.hand:
				if card > comm.card:
					playCard = card
					break

		print("playCard: " + str(playCard))
		lastPlayed = playCard
		comm.playCard(playCard)
		self.counter.updateDeck(playCard)
		
	def challenged(self, comm): 
		if (self.calc_challenge(comm) > 3):
			comm.acceptChallenge()
		else:
			comm.rejectChallenge()

	def result(self, comm):
		if comm.player_num == 0 and (comm.resultType == "trick_won" or comm.resultType == "trick_tied"):
			self.counter.updateDeck(comm.card)
			self.opponent_cards.append(comm.card)
		if comm.resultType == "hand_done":
			self.opponent_cards = []

	def calc_challenge(self, comm):
		numCards = 0
		avg = self.counter.getAvg()
		print("avg: " + str(avg))
		for card in comm.hand:
			if (card > avg):
				numCards += 1
		print(numCards)
		return numCards + comm.your_tricks