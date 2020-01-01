from deck import Deck

# Hold 'em
class NLHE():
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.hands = []
		self.community = []
		self.cards_per_hand = 2
		self.players = 0
		self.pot = 0

	'''
	player: id for player for self.hands
	community: community cards
	'''
	def score_hand(self, player):
