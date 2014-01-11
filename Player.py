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
		
		#normal play
		playCard = 0
		comm.hand.sort()
		maxdiff = 4
		option = 0
		tied_tricks = comm.total_tricks - comm.their_tricks - comm.your_tricks
		if tied_tricks == 1:
			comm.total_tricks = 0
		elif tied_tricks == 2 or tied_tricks == 3:
			comm.your_tricks += 1
			comm.their_tricks += 1
			
		if comm.total_tricks == 0:
			if comm.card == None:
				playCard = self.MidCard(comm, avg)
			else:
				playCard = self.WinifDiff(comm, maxdiff)
				# playCard = WinorLowest(comm)
		
		elif comm.total_tricks == 1:
			if comm.your_tricks == 1:
				playCard = self.LowCard(comm)
			elif comm.their_tricks == 1:
				playCard = self.WinifDiff(comm, maxdiff)
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
				playCard = self.WinorLowest(comm, maxdiff)
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
				playCard = self.WinorLowest(comm)
			
		elif comm.total_tricks == 2:
			
			
			
			
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
		
	#different actions for each situation in normal play
	#you starts
	def WinorLowest(self, comm):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] > comm.card 
				cardindex = x
				break
		return cardindex
	def WinifDiff(self, comm, diff):
		cardindex = 0
		for x in range(0,len(comm.hand)):
			if comm.hand[x] >= comm.card #allows ties
				if comm.hand[x] - comm.card <= diff:
					cardindex = x
					break
		return cardindex
		
	#I starts no comm.card
	def LowCard(self, comm):
		cardindex = 0
		return cardindex
	def HighCard(self, comm):
		cardindex = len(comm.hand)
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