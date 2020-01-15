from deck import Deck

# Hold 'em
# Max 9-Handed
class NLHE():
	def __init__(self, sb=1, bb=2):
		self.deck = Deck()
		self.deck.shuffle()

		self.hands = []
		self.community = []
		
		self.cards_per_hand = 2
		self.players = []
		self.num_players = 0
		self.pot = 0
		self.small_blind = sb
		self.big_blind = bb

	
	def add_player(self, player):
		if self.num_players == 9:
			return False
		self.players.append(player)
		self.num_players += 1
		return True


	'''
	player: id for player for self.hands
	community: community cards
	'''
	def score_hand(self, player):
		pass