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

	def playRequest(self, comm):
	#refreshes deck every 10 hands and removes cards in hand
		if comm.hand_id %10 == 1 and comm.total_tricks == 0:
			self.counter.refreshDeck()
			for i in range (0,len(comm.hand)):
				self.counter.updateDeck(comm.hand[i])
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

		print(comm.hand)
		# print("Hand Value: " + str(Prob.Prob.handValue(self.counter, comm)))
		playCard = 0
		comm.hand.sort()
		if (comm.card == None):
			indexClosest = 0
			diff = 13
			for x in range(0,math.ceil(len(comm.hand)/2)):
				if abs(comm.hand[x] - 6) < diff:
					indexClosest = x
					diff = abs(comm.hand[x] - 6)
#			playCard = int(math.floor(int(len(comm.hand)) / 2))
			playCard = indexClosest
		else:
			if comm.your_tricks > comm.their_tricks:
				# play lowest card
				playCard = 0
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
		numCards = 0
		avg = self.counter.getAvg()
		print("avg: " + str(avg))
		for card in comm.hand:
			if (card > avg):
				numCards += 1
		print(numCards)
		return numCards + comm.your_tricks

		#return list 1, 2, 3, 4, 5 card average
	def CalcUpperCards(self, comm):
		comm.hand.sort()
		avgs = None
		for i in xrange(0,len(comm.hand)):
			sum = 0
			for j in xrange(i,len(comm.hand)):
				sum += comm.hand[j]
			avgs.insert(0,sum)
		for k in xrange(0, 5-len(comm.hand)):
			avgs.append(0)
		return avgs