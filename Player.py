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

		print(comm.hand)
		print("Hand Value: " + str(Prob.Prob.handValue(counter, comm)))
		playCard = 0
		comm.hand.sort()
		if (comm.card == None):
			playCard = int(math.floor(len(comm.hand) / 2))
		else:
			for i in range(len(comm.hand)):
				if comm.hand[i] > comm.card:
					playCard = i
					break

		print("playCard: " + str(playCard))
		lastPlayed = comm.hand[playCard]
		comm.playCard(comm.hand[playCard])
		self.counter.updateDeck(comm.hand[playCard])
		
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
