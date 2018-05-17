class Board:
	"""The game board."""
	def __init__(self):
		self.board_size = 8
		self.tiles = [[None] * self.board_size] * self.board_size

