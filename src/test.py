import sys
from hand_rank import Hand_Rank
from card import Card

def parse_card_str(card_str):
    return Card(int(card_str[:-1]), card_str[-1])

def parse_cards_str(cards_str):
    return [parse_card_str(x.strip()) for x in cards_str.split(',')]

if __name__ == '__main__':
    # Hand Rank Testing
    # Straight Flush
    cards_strs = [
                    "2C,3C,4C,5C,6C,10S,14H", # straight flush
                    "2C,3C,4C,5C,6H,10S,14C", # straight flush wrap arround
                    "2C,3C,2H,2S,2D,5C,8D", # quads
                 ]
    for cards_str in cards_strs:
        temp = Hand_Rank(parse_cards_str(cards_str))
        print(temp)