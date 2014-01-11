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
		self.playerlead = None # me or notme as to who played the first card of the trick
		self.deckAvg = 6
		self.alpha = 0.5
		self.beta = 0.02
		self.epsilon = 0.05

	def playRequest(self, comm):
	#refreshes deck every 10 hands and removes cards in hand

		if comm.total_tricks == 0:
			if comm.hand_id % 10 == 1:
				self.counter.refreshDeck()
			for i in range(0, len(comm.hand)):
				self.counter.updateDeck(comm.hand[i])
			self.deckAvg = self.counter.getAvg()

		#card counting update when other plays first
		if comm.card != None:
			self.playerlead = "notme"
			self.counter.updateDeck(comm.card)
			self.opponent_cards.append(comm.card)
		else:
			self.playerlead = "me"

		#challenge logic
		if comm.can_challenge and self.calc_challenge(comm) > 3:
			comm.sendChallenge()
			return

		# normal playing
		playCard = 0
		comm.hand.sort()
		if (comm.card == None):
			indexClosest = 0
			diff = 13
			for x in range(0,len(comm.hand)):
				if abs(comm.hand[x] - self.deckAvg) < diff:
					indexClosest = x
					diff = abs(comm.hand[x] - self.deckAvg)
#			playCard = int(math.floor(int(len(comm.hand)) / 2))
			playCard = indexClosest
		else:
			for x in range(0,len(comm.hand)):
				if comm.hand[x] > comm.card:
					playCard = x
					break
		print("playCard: " + str(comm.hand[playCard]))

		self.lastPlayed = comm.hand[playCard]
		comm.playCard(comm.hand[playCard])
		
	def challenged(self, comm): 
		if (self.calc_challenge(comm) > 3):
			comm.acceptChallenge()
		else:
			comm.rejectChallenge()

	def result(self, comm):
		if self.playerlead == "me":
			if comm.resultType == "trick_won":
				self.counter.updateDeck(comm.card)
				self.opponent_cards.append(comm.card)
			elif comm.resultType == "trick_tied":
				self.counter.updateDeck(self.lastPlayed)
			if comm.resultType == "hand_done":
				self.opponent_cards = []
		# if comm.player_num == 0 and (comm.resultType == "trick_won" or comm.resultType == "trick_tied"):
			# self.counter.updateDeck(comm.card)
			# self.opponent_cards.append(comm.card)
		# if comm.resultType == "hand_done":
			# self.opponent_cards = []

	def calc_challenge(self, comm):
		total = 0;
		for card in self.opponent_cards:
			total += card

		estimate = (5 * self.deckAvg - total) / (5 - comm.total_tricks)


		numCards = 0
		for card in comm.hand:
			if (card > estimate + self.alpha - (self.beta * comm.total_tricks) + (self.epsilon * (comm.your_points - comm.their_points))):
				numCards += 1

		return numCards + comm.your_tricks
