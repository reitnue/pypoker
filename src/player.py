import sys

class NLHEPlayer():
	def __init__(self, buyin):
		self.stack = buyin
		self.hole_cards = []
		self.position = None
		self.game = None # 1 game per player

	def sit_down(self, game):
		if not self.game and self.game.add_player(player):
			self.game = game
		else:
			sys.stderr.write("Already in a game\n")

