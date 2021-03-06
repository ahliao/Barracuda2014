import socket
import json
import struct
import time
import sys

import socketLayer
import Player

class Comm:
	def __init__(self):
		self.s = socketLayer.SocketLayer("cuda.contest", 9999)

		# "request", "result", "error"
		self.type = None

		# "trick_won", "trick_tied", "hand_won", "game_won", "error"
		self.resultType = None

		# if resultType == error, gives reason
		self.reason = None

		# will be either "request_card" or "challenge_offered"
		self.request = None

		# remaining time
		self.remaining = None

		# request_id
		self.request_id = None

		# array with hand
		self.hand = None

		# card on the table
		self.card = None

		# hand id
		self.hand_id = None

		# game id
		self.game_id = None

		# number of tricks you won
		self.your_tricks = None

		# number of tricks they've won
		self.their_tricks = None

		# number of tricks played
		self.total_tricks = None

		# a boolean
		self.can_challenge = None

		# in challenge
		self.in_challenge = None

		# your points
		self.your_points = None

		# their points
		self.their_points = None

		# opponent id
		self.opponent_id = None

		# player num
		self.player_number = None

		self.host = None

		self.by = None
		
	# gets next message in socket
	def refresh(self, player):
		msg = self.s.pump()

		self.type = msg["type"]
		if (self.type == "request"):
			self.request = msg["request"]
			self.remaining = msg["remaining"]
			self.request_id = msg["request_id"]
			self.hand = msg["state"]["hand"]

			try: 
				self.card = msg["state"]["card"]
			except:
				self.card = None

			self.hand_id = msg["state"]["hand_id"]
			self.game_id = msg["state"]["game_id"]
			self.your_tricks = msg["state"]["your_tricks"]
			self.their_tricks = msg["state"]["their_tricks"]
			self.can_challenge = msg["state"]["can_challenge"]
			self.in_challenge = msg["state"]["in_challenge"]
			self.total_tricks = msg["state"]["total_tricks"]
			self.your_points = msg["state"]["your_points"]
			self.opponent_id = msg["state"]["opponent_id"]
			self.their_points = msg["state"]["their_points"]
			self.player_num = msg["state"]["player_number"]
			self.game_id = msg["state"]["game_id"]
			
		elif (self.type == "result"):
			self.resultType = msg["result"]["type"]
			self.player_num = msg["your_player_num"]
			if (self.resultType == "trick_won" or self.resultType == "hand_done" or self.resultType == "game_won"):
				try:
					self.by = msg["result"]["by"]
				except:
					self.by = None

			if (self.resultType == "trick_won"):
				self.card = msg["result"]["card"]
			elif (self.resultType == "trick_tied"):
				self.card = player.lastPlayed
		elif (self.type == "error"):
			self.host = msg["seen_host"]

	# sends information
	def acceptChallenge(self):
		self.s.send({"type": "move", "request_id": self.request_id, "response": {"type": "accept_challenge"}})

	def rejectChallenge(self):
		self.s.send({"type": "move", "request_id": self.request_id, "response": {"type": "reject_challenge"}})

	def sendChallenge(self):
		self.s.send({"type": "move", "request_id": self.request_id, "response": {"type": "offer_challenge"}})

	def playCard(self, card):
		self.s.send({"type": "move", "request_id": self.request_id, "response": {"type": "play_card", "card": card}})

	def getWinner(self):
		try:
			if (self.player_num == self.by):
				return True
			else:
				return False
		except:
			print("error getting winner")
