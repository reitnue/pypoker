import sys

# from deck import Deck
from card import SUITS, RANKS
from card import Card
from poker import Poker
'''
1. Game Play first
2. Betting
'''

NLHE_HAND_RANKS = {
                    "STRAIGHT_FLUSH" : 8,
                    "QUADS"          : 7,
                    "FULL_HOUSE"     : 6,
                    "FLUSH"          : 5,
                    "STRAIGHT"       : 4,
                    "TRIPS"          : 3,
                    "TWO_PAIR"       : 2,
                    "PAIR"           : 1,
                    "HIGH"           : 0,
                  }

NLHE_HAND_RANK_REPR = {v : k for k, v in NLHE_HAND_RANKS.items()}

# Hold 'em
# Max 9-Handed
class Hand_Rank():
    '''
    players: list of player objects - starts with small blind...
    '''
    def __init__(self, cards):
        self.value = 0
        self.hand_rank = 0
        self.cards = cards
        self.top_ranks = []
        self.score_hand()
        self.calculate_hand_value()

    '''
    player: id for player for self.hands
    community: community cards
    '''
    def score_hand(self):
        cards = self.cards
        
        # suited?
        FLUSH = False
        flush_hand = []
        flush_suit = None
        
        suit_dict = dict(zip(SUITS, [0] * len(SUITS)))
        rank_dict = dict(zip(RANKS, [0] * len(RANKS)))
        rank_indicator_arr = [0] * len(RANKS)
        
        ranks_arr = sorted([x.get_rank() for x in cards])[::-1]

        for card in cards:
            suit_dict[card.get_suit()] += 1
            rank_dict[card.get_rank()] += 1
            rank_indicator_arr[card.get_rank()-2] = 1

        # return flush, flush_hand, flush_suit
        STRAIGHT_FLUSH = False
        QUADS          = False
        FULL_HOUSE     = False
        FLUSH          = False
        STRAIGHT       = False
        TRIPS          = False
        TWO_PAIR       = False
        PAIR           = False
        
        straight_flush_high = None

        quad_rank = None

        full_rank = None
        other_rank = None
        
        flush_suit = None
        flush_cards = []

        straight_highs = []
        straight_high = None

        trip_ranks = []
        trip_rank = None
        
        pair_ranks = []
        pair_rank = None
        
        two_pair_ranks = []
        
        kickers = []
        
        if rank_indicator_arr[-1] == 1 and sum(rank_indicator_arr[:4]) == 4:
            straight_highs.append(5)

        for i in range(len(rank_indicator_arr) - 5):
            next_sum = sum(rank_indicator_arr[i:i+5])
            if next_sum == 5: # straight!
                straight_highs.append(i+6)

        for suit in SUITS:
            if suit_dict[suit] > 4:
                FLUSH = True
                flush_suit = suit

        for high in straight_highs[::-1]: # in reverse order
            temp_straight_flush = True
            if high == 5:
                temp_straight_flush &= Card(14, flush_suit) in cards
                for i in range(2, 6):
                    temp_straight_flush &= Card(i, flush_suit) in cards
            else:
                for i in range(high-4, high+1):
                    temp_straight_flush &= (Card(i, flush_suit) in cards)

            if temp_straight_flush:
                straight_flush_high = high
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['STRAIGHT_FLUSH'])
                self.top_ranks = [high]
                return


        for rank in RANKS[::-1]:
            if rank_dict[rank] == 4:
                QUADS = True
                quad_rank = rank
                # kicker
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['QUADS'])
                for _ in range(4):
                    ranks_arr.remove(quad_rank)
                self.top_ranks = [quad_rank] + [ranks_arr[0]]

                return
            elif rank_dict[rank] == 3:
                TRIPS = True
                trip_ranks.append(rank)
            elif rank_dict[rank] == 2:
                PAIR = True
                pair_ranks.append(rank)

        # HAND RANK FLOW LIST

        # trip, pair_ranks will already by sorted
        if not QUADS:
            if len(trip_ranks) > 0:
                FULL_HOUSE = True
                full_rank = trip_ranks[0]

                other_rank = pair_ranks[0]
                if len(trip_ranks) > 1:
                    other_rank = max(trip_ranks[1], other_rank)

                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['FULL_HOUSE'])
                self.top_ranks = 3*[full_rank] + 2*[other_rank]
                return
        
        if not FULL_HOUSE:
            if FLUSH:
                flush_cards = sorted(filter((lambda x: x.get_suit() == flush_suit), cards))
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['FLUSH'])
                self.top_ranks = sorted([x.get_rank() for x in flush_cards])[::-1][:5]
                return

        if not FLUSH:
            if straight_highs:
                straight_high = straight_highs[-1]
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['STRAIGHT'])
                self.top_ranks = straight_high
                return

        if not STRAIGHT:
            if len(trip_ranks) > 0:
                TRIPS = True
                trip_rank = trip_ranks[0]
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['TRIPS'])
                for _ in range(3):
                    ranks_arr.remove(trip_rank)
                self.top_ranks = [trip_rank] + ranks_arr[:2]
                return

        if not TRIPS:
            if len(pair_ranks) > 1:
                TWO_PAIR = True
                two_pair_ranks = pair_ranks[:2]
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['TWO_PAIR'])
                for _ in range(2):
                    ranks_arr.remove(two_pair_ranks[0])
                    ranks_arr.remove(two_pair_ranks[1])
                self.top_ranks = two_pair_ranks + [ranks_arr[0]]
                return

        if not TWO_PAIR:
            if len(pair_ranks) == 1:
                PAIR == True
                pair_rank = pair_ranks[0]
                self.hand_rank = max(self.hand_rank, NLHE_HAND_RANKS['PAIR'])
                for _ in range(2):
                    ranks_arr.remove(pair_rank)
                self.top_ranks = [pair_rank] + ranks_arr[:3]
                return

        if not PAIR:
            kickers = sorted(cards, reverse=True)[:5]
                # High Card
            self.top_ranks = ranks_arr[:5]

            return

    # run after score_hand
    def calculate_hand_value(self):
        self.value += self.hand_rank * (10**5)
        kickers = self.top_ranks + [0]*(5 - len(self.top_ranks))
        for index, kicker in enumerate(kickers[::-1]):
            self.value += kicker * (10 ** index)

    def __str__(self):
        return str(self.value) + ' - ' + NLHE_HAND_RANK_REPR[self.hand_rank] + ' ' + str(self.top_ranks)

    def __eq__ (self, other):
        return (self.value == other.value)

    def __ne__ (self, other):
        return (self.value != other.value)

    def __lt__ (self, other):
        return (self.value < other.value)

    def __le__ (self, other):
        return (self.value <= other.value)

    def __gt__ (self, other):
        return (self.value > other.value)

    def __ge__ (self, other):
        return (self.value >= other.value)

if __name__ == '__main__':
    flops = [[Card(2, 'C'), Card(2, 'H'), Card(3, 'H'), Card(5, 'S'), Card(9, 'S'), Card(10, 'S')],
             [Card(2, 'C'), Card(2, 'H'), Card(3, 'H'), Card(5, 'S'), Card(5, 'S'), Card(10, 'S')],]
    temp1 = Hand_Rank(flops[0])
    temp2 = Hand_Rank(flops[1])
    
    print(temp1 > temp2)
    for flop in flops:
        temp = Hand_Rank(flop)
        print(temp)