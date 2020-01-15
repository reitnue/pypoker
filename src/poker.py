import sys

from deck import Deck

'''
1. Game Play first
2. Betting
'''

# Hold 'em
# Max 9-Handed
class Poker():
    '''
    players: list of player objects - starts with small blind...
    '''
    def __init__(self, players):
        self.deck = Deck()
        self.deck.shuffle()

        self.players = players
        self.num_players = len(players)

        self.hands = [[] for _ in players]
        self.folded = [0 for _ in players]

        self.pot = 0

    def score_hand(self):
        pass

    # def 