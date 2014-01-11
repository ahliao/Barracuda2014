m operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction

def nCk(n,k): 
	return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1) )

def cardValue(cardVal, count, comm):
	betterCards = 0
	for x in range(0,cardVal):
		betterCards += count.deck[x]
#probBetter = nCk(betterCards, 1) * nCk(count.numCards-betterCards, len(comm.hand)-1)
	probBetter = nCk(betterCard, len(comm.hand)) / nCk(count.numCards, len(comm.hand))
	return 1-probBetter

def handValue(count, comm):
	totalVal = 0
	for x in range(0,len(comm.hand)):
		totalVal *= cardValue(comm.hand[x], count, comm)
# Just multiplying for now
