import sys
import random

from card import Card, SUITS, RANKS

class Deck: # no joker
	def __init__(self):
		self.deck = []
		for rank in RANKS:
			for suit in SUITS:
				self.deck.append(Card(rank, suit))

	def __len__(self):
		return len(self.deck)

	def shuffle(self):
		random.shuffle(self.deck)


