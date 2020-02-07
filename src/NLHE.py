import sys

# from deck import Deck
from card import SUITS, RANKS
from card import Card
from poker import Poker
from hand_rank import Hand_Rank
from player import NLHEPlayer
from player import FOLD, CHECK, CALL, RAISE


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

    def hand_end(self):
        return len(list(filter((lambda x: x >= 0), self.bets))) == 1

    def is_action_done(self):
        # remove negative, (use -(1e-9) for folding with 0)
        return len(set(filter((lambda x: x>=0), self.bets))) == 1

    def betting(self, hand_round=0): # 0 -pre, 1 -flop, 2 -turn, 3 -river
        if hand_round == 0:
            # blinds - [1, 2, 0, ...]
            self.bets[0] += min(self.small_blind, self.players[0].stack)
            self.bets[1] += min(self.big_blind, self.players[1].stack)

        action_on = 0
        # pre-flop betting
        # second condition only for preflop
        while not self.is_action_done() or (action_on == 1 and self.bets[action_on] == 2 and hand_round == 0):
            # print(action_on)
            if self.bets[action_on] >= 0:
                player_action, amount = self.players[action_on].action([], 0, action_on, self.community)
                
                if player_action == CALL:
                    self.bets[action_on] = max(self.bets)
                
                elif player_action == CHECK:
                    if self.bets[action_on] == max(self.bets): # check
                        pass
                    else:
                        if self.best[action_on] == 0:
                            self.best[action_on] = (1e-9)
                        self.best[action_on] *= -1 # fold
                
                elif player_action == RAISE:
                    self.bets[action_on] = amount + max(self.bets)

            action_on += 1
            action_on %= len(self.players)
        # print(self.bets)
        return self.hand_end()

    def play(self):
        # deal hands
        for i in range(self.num_players):
            for _ in range(self.cards_per_hand):
                self.hands[i].append(self.deck.deal())
        
        if self.betting(hand_round=0):
            print('end pre-flop')

        # return 
        # flop
        for _ in range(3):
            self.community.append(self.deck.deal())

        if self.betting(hand_round=1):
            print('end', 'flop')

        # turn
        for _ in range(1):
            self.community.append(self.deck.deal())

        if self.betting(hand_round=2):
            print('end', 'turn')

        # river
        for _ in range(1):
            self.community.append(self.deck.deal())

        if self.betting(hand_round=3):
            print('end', 'river')

        self.pot = sum(map(abs, map(int, self.bets)))
        for player_id in self.show_rankings():
            self.players[player_id].receive(int(self.pot / len(self.show_rankings())))

        for player_id, bet in enumerate(self.bets):    
            self.players[player_id].pay(abs(int(bet)))

        # print(self.show_rankings())
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

    def show_rankings(self):
        hand_ranks = {}
        for player, cards in enumerate(self.hands):
            hand_rank = Hand_Rank(self.community + cards)
            # print(player, hand_rank)
            hand_value = int(hand_rank)

            if hand_value not in hand_ranks:
                hand_ranks[hand_value] = []
            hand_ranks[hand_value].append(player)
        
        return hand_ranks[max(list(hand_ranks.keys()))]

if __name__ == '__main__':
    buyin = 20
    players = [NLHEPlayer(buyin), NLHEPlayer(buyin)]

    num = 2
    for _ in range(1000):
        game = NLHE(players)
        game.play()
    for player in players:
        print(player.stack)
    # game.show_hands()
    # game.show_community()
    # print(game.show_rankings())