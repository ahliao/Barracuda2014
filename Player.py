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
		comm.playCard(comm.hand[0])
		
	def challenged(self, comm):
		comm.acceptChallenge()

	def result(self, comm):
		pass
		
	

