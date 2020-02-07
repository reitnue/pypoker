import sys

FOLD = 0
CHECK = 0
CALL = 1
RAISE = 2

class NLHEPlayer():
    def __init__(self, buyin):
        self.stack = buyin
        self.hole_cards = []

    def action(self, others, hand_round, position, community):
        # return RAISE, 10

        # get the amount you are raising/calling

        return CALL, 0 # calls the bet

    def pay(self, amount):
        self.stack -= amount # error check

    def receive(self, amount):
        self.stack += amount # logging