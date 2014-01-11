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
		self.alpha = 1.5 # base tolerance
		self.beta = 0.15
		self.epsilon = 0.25

	def playRequest(self, comm):
	#refreshes deck every 10 hands and removes cards in hand

		if comm.total_tricks == 0:
			self.opponent_cards = []
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
		if comm.can_challenge and comm.total_tricks != 0 and self.calc_challenge(comm) > 2:
			comm.sendChallenge()
			return

		# normal playing
# 		playCard = 0
# 		comm.hand.sort()
# 		if (comm.card == None):
# 			indexClosest = 0
# 			diff = 13
# 			for x in range(0,math.ceil(len(comm.hand)/2)):
# 				if abs(comm.hand[x] - self.deckAvg) < diff:

# 					indexClosest = x
# 					diff = abs(comm.hand[x] - self.deckAvg)
# #			playCard = int(math.floor(int(len(comm.hand)) / 2))
# 			playCard = indexClosest
# 		else:
# 			if comm.your_tricks > comm.their_tricks:
# 				# play lowest card
# 				playCard = 0

# 		print(comm.hand)

		#normal play
		playCard = 0
		comm.hand.sort()

		
		# if comm.total_tricks == 0:
		# 	if comm.card == None:
		# 		if comm.hand[1] - comm.hand[0] > 3: 
		# 			playCard = self.MidCard(comm, self.deckAvg)
		# 		else:
		# 			playCard = 1
		# 	else:
		# 		playCard = self.WinifDiff(comm, 4)

		maxdiff = 3
		tied_tricks = comm.total_tricks - comm.their_tricks - comm.your_tricks
		if tied_tricks == 1:
			comm.total_tricks = 0
		elif tied_tricks == 2 or tied_tricks == 3:
			comm.your_tricks += 1
			comm.their_tricks += 1
			
		if comm.total_tricks == 0:
			if comm.card == None: # our lead
				playCard = self.MidCard(comm, self.deckAvg)#self.LowCard(comm)
			else: # their lead
				playCard = self.WinifDiffnotEqual(comm, maxdiff)
				#playCard = self.WinorLowest(comm)
		
		elif comm.total_tricks == 1:
			if comm.your_tricks == 1: # and their_tricks == 0
				playCard = self.LowCard(comm)
			elif comm.their_tricks == 1: # and our_tricks == 0
				playCard = self.WinifDiffnotEqual(comm, maxdiff)

		# 		playCard = self.WinifDiff(comm, 4)
		# 		# playCard = WinorLowest(comm)
		# 	else: #tied?
		# 		if comm.card == None:
		# 			#pass
		# 			playCard = self.MidCard(comm, self.deckAvg)
		# 		else:
		# 			playCard = self.WinifDiff(comm, 4)
		# 			# playCard = WinorLowest(comm)
			
		# elif comm.your_tricks >= 2:
		# 	if comm.card == None:
		# 		playCard = self.LowCard(comm)
		# 	else:
		# 		playCard = self.WinorLowest(comm)
				
		# elif comm.their_tricks == 2:
		# 	if comm.card == None:
		# 		playCard = self.HighCard(comm)
		# 	else:
		# 		playCard = self.WinorLowest(comm)

				# playCard = WinorLowest(comm)
			else: #tied?
				if comm.card == None:
					playCard = self.MidCard(comm, avg)
				else:
					playCard = self.WinifDiff(comm, maxdiff)
					# playCard = WinorLowest(comm)
		
		elif comm.your_tricks == 1 and comm.their_tricks == 1:
			if comm.card == None:
				playCard = self.LowCard(comm)
			else:
				playCard = self.WinifDiff(comm, maxdiff)
				# playCard = WinorLowest(comm)
				
		elif comm.your_tricks >= 2:
			if comm.card == None:
				playCard = self.LowCard(comm)
			else:
				playCard = self.WinorLowest(comm)
				
		elif comm.their_tricks >= 2:
			if comm.card == None:
				playCard = self.HighCard(comm)
			else:
				#playCard = self.WinifDiff(comm, maxdiff)
				playCard = self.WinorLowestnoTie(comm)
			
		# elif comm.total_tricks == 2:
			
			
			
			
		# elif comm.total_tricks > 2:
			# if comm.card == None:
				# playCard = self.HighCard(comm)
			# else:
				# playCard = self.WinorLowest(comm)

			
			
		# if (comm.card == None):
		# else:
			# if comm.your_tricks > comm.their_tricks:
				#play lowest card
				# playCard = 0
			# else:
				# for x in range(0,len(comm.hand)):
					# if comm.hand[x] > comm.card:
						# playCard = x
						# break

		self.lastPlayed = comm.hand[playCard]
		comm.playCard(comm.hand[playCard])
		
	def challenged(self, comm): 
		if (self.calc_challenge(comm, True) > 2):
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
				self.opponent_cards.append(self.lastPlayed)
			if comm.resultType == "hand_done":
				self.opponent_cards = []
		# if comm.player_num == 0 and (comm.resultType == "trick_won" or comm.resultType == "trick_tied"):
			# self.counter.updateDeck(comm.card)
			# self.opponent_cards.append(comm.card)
		# if comm.resultType == "hand_done":
			# self.opponent_cards = []

	def calc_challenge(self, comm, challenged = False):
		if (comm.their_points == 9):
			return 5

		if comm.their_tricks == 2 and comm.your_tricks == 2:
			if comm.hand[0] > 9:
				return 5
			else:
				return 0
				
		if comm.your_tricks == 2 and comm.hand[len(comm.hand)-1] == 13:
			return 5


		total = 0;
		for card in self.opponent_cards:
			total += card
		print(self.opponent_cards)

		if len(self.opponent_cards) == 5:
			return 0

		estimate = (5 * self.deckAvg - total) / (5 - len(self.opponent_cards))
		if (estimate > 13):
			estimate = 12

		print("total: " + str(total))

		print("deckAvg: " + str(self.deckAvg))
		print("avg: " + str(estimate))
		a = self.alpha
		b = self.beta * comm.total_tricks
		print("total tricks: " + str(comm.total_tricks))
		c = self.epsilon * (comm.your_points - comm.their_points)
		estimate += a - b + c

		if challenged:
			estimate += .5

		if comm.your_points == 9 and comm.their_points >= 6:
			estimate -= 1.2

		if comm.your_tricks == 2 and comm.their_tricks == 0:
			return 5

		print("threshold: " + str(estimate))



		numCards = 0


		# beat = -1
		# # if there is a card on the field
		# if (comm.card != None):
		# 	for i in range(len(comm.hand)):
		# 		if comm.hand[i] > comm.card:
		# 			beat = i
		# 			numCards += 1
		# 			break


		# for i in range(len(comm.hand)):
		# 	if (comm.hand[i] > estimate and i != beat):
		# 		numCards += 1

		if len(comm.hand) == 1 and comm.card != None and comm.your_tricks >= 2:
			if comm.hand[0] >= comm.card:
				return 5

		if (comm.your_tricks == 2 and (comm.their_tricks == 1 or comm.their_tricks == 0) and len(comm.hand) == 1):
			return 5

		for card in comm.hand:
			if (card > estimate):
				numCards += 1

		print(numCards + comm.your_tricks)


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
		
	#different actions for each situation in normal play
	#you starts
	def WinorLowest(self, comm):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] > comm.card: 
				cardindex = x
				break
		return cardindex

	def WinorLowestnoTie(self, comm):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] >= comm.card: 
				cardindex = x
				break
		return cardindex

	def WinifDiff(self, comm, diff):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] >= comm.card: #allows ties
				if comm.hand[x] - comm.card <= diff:
					cardindex = x
					break
		return cardindex

	def WinifDiffnotEqual(self, comm, diff):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] > comm.card: #allows ties
				if comm.hand[x] - comm.card <= diff:
					cardindex = x
					break
		return cardindex
		
	#I starts no comm.card
	def LowCard(self, comm):
		cardindex = 0
		return cardindex
	def HighCard(self, comm):
		cardindex = len(comm.hand)-1
		return cardindex
	def MidCard(self, comm, avg):
		indexClosest = 0
		diff = 13 #max diff
		for x in range(0,math.ceil(len(comm.hand)/2)):
			if abs(comm.hand[x] - avg) < diff:
				indexClosest = x
				diff = abs(comm.hand[x] - avg)
		cardindex = indexClosest
		return cardindex
