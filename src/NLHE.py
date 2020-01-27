import sys

# from deck import Deck
from card import SUITS, RANKS
from card import Card
from poker import Poker
'''
1. Game Play first
2. Betting
'''

# Hold 'em
# Max 9-Handed
class NLHE(Poker):
    '''
    players: list of player objects - starts with small blind...
    '''
    def __init__(self, players, sb=1, bb=2):
        super(NLHE, self).__init__(players)
        self.community = []
        
        self.cards_per_hand = 2

        self.small_blind = sb
        self.big_blind = bb

    def play(self):
        # deal hands
        for i in range(self.num_players):
            for _ in range(self.cards_per_hand):
                self.hands[i].append(self.deck.deal())

        # flop
        for _ in range(3):
            self.community.append(self.deck.deal())
        # turn
        for _ in range(1):
            self.community.append(self.deck.deal())
        # river
        for _ in range(1):
            self.community.append(self.deck.deal())

        return

    def show_community(self):
        for i in range(5):
            if len(self.community) > i:
                sys.stdout.write(str(self.community[i])+" ")
            else:
                sys.stdout.write('___ ')
        print('')

    def show_hands(self):
        for i in range(len(self.players)):
            print(i, self.hands[i][0], self.hands[i][1])

        return

if __name__ == '__main__':
    num = 5
    game = NLHE(list(range(num)))
    game.play()
    game.show_hands()
    game.show_community()
