import unittest
from alphaTsuro.Tile import Tile
from alphaTsuro.Deck import Deck
from alphaTsuro.Board import Board
from alphaTsuro.Piece import Piece


class TestDeckLoading(unittest.TestCase):
	def setUp(self):
		self.filename = "data/testDeck.json"

	def test_deck_loading(self):
		testDeck = Deck.from_json(self.filename)
		self.assertEqual(len(testDeck.tiles), 2)

class TestPieceMovement(unittest.TestCase):
	def setUp(self):
		self.board = Board()
		self.tile1 = Tile()
		self.tile1.connections = {"UL":"LU", "UR":"RD", "RU":"DL", "RD":"UL",
								  "DR":"LD", "DL":"RU", "LD":"DR", "LU":"UL"}
		self.tile2 = Tile()
		self.tile2.connections = {"UL":"DR", "UR":"DL", "RU":"RD", "RD":"RU",
								  "DR":"UL", "DL":"UR", "LD":"LU", "LU":"LD"}
		self.tile3 = Tile()
		self.tile3.connections = {"UL":"RU", "UR":"DR", "RU":"UL", "RD":"LD",
								  "DR":"UR", "DL":"LU", "LD":"RD", "LU":"DL"}
		self.piece = Piece(self.board, 0, 0, "UR")

	def test_piece_movement(self):
		self.board.tiles[0][0] = self.tile3
		self.board.tiles[1][0] = self.tile1
		self.board.tiles[1][1] = self.tile2
		self.piece.update_position()
		self.assertEqual(self.piece.row, 2)
		self.assertEqual(self.piece.col, 0)
		self.assertEqual(self.piece.edge_position, "UL")

	def test_on_board(self):
		self.assertTrue(self.piece.on_board())
		(self.piece.row, self.piece.col) = (-1,0)
		self.assertFalse(self.piece.on_board())
		(self.piece.row, self.piece.col) = (0,-1)
		self.assertFalse(self.piece.on_board())
		(self.piece.row, self.piece.col) = (-1,0)
		self.assertFalse(self.piece.on_board())
		(self.piece.row, self.piece.col) = (7,7)
		self.assertTrue(self.piece.on_board())
		(self.piece.row, self.piece.col) = (7,8)
		self.assertFalse(self.piece.on_board())
		(self.piece.row, self.piece.col) = (8,7)
		self.assertFalse(self.piece.on_board())