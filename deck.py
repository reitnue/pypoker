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

    def deal(self):
        if len(self) != 0:
            return self.deck.pop()
        return None

if __name__ == '__main__':
    random.seed(0)
    temp = Deck()
    temp.shuffle()
    
    for _ in range(2):
        print(temp.deal())