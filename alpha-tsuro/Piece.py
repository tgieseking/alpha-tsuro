from Board import Board

class Piece:
	"""A game piece"""
	def __init__(self, board, row, col, edge_position):
		if row < 0 or row >= board.board_size:
			raise InvalidPositionException
		if col < 0 or col >= board.board_size:
			raise InvalidPositionException
		if not edge_position in {"UL", "UR", "RU", "RD", "DR", "DL", "LD", "LU"}:
			raise InvalidPositionException
			
		self.board = board
		self.row = row
		self.col = col
		self.edge_position = edge_position

class InvalidPositionException(Exception):
	"""Thrown when a game piece is initialized to a position outsize the game board"""
	pass