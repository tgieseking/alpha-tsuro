import unittest
from alphaTsuro.Tile import Tile
from alphaTsuro.Deck import Deck
from alphaTsuro.Board import Board
from alphaTsuro.Piece import Piece


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.filename = "data/testDeck.json"
        self.test_deck = Deck()
        self.test_deck.tiles = [1,2,3,4,5]

    def test_deck_loading(self):
        testDeck = Deck.from_json(self.filename)
        self.assertEqual(len(testDeck.tiles), 2)

    def test_shuffle(self):
        shuffled = False
        for i in range(10):
            self.test_deck.shuffle()
            shuffled = shuffled or self.test_deck.tiles != [1,2,3,4,5]
            self.assertEqual(sorted(self.test_deck.tiles), [1,2,3,4,5])
        self.assertTrue(shuffled)

class TestPieceMovement(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.tile1 = Tile()
        self.tile1.connections = {"UL":"LU", "UR":"RD", "RU":"DL", "RD":"UR",
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

class TestTile(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile()
        self.tile1.connections = {"UL":"LU", "UR":"RD", "RU":"DL", "RD":"UR",
                                  "DR":"LD", "DL":"RU", "LD":"DR", "LU":"UL"}

    def test_single_rotation(self):
        self.tile1.rotate_clockwise()
        self.assertEqual(self.tile1.connections, {"UL":"LD", "UR":"RU", "RU":"UR", "RD":"DL",
                                             "DR":"LU", "DL":"RD", "LD":"UL", "LU":"DR"})

    def test_multiple_rotation(self):
        self.tile1.rotate_clockwise(7)
        self.assertEqual(self.tile1.connections, {"UL":"RD", "UR":"LU", "RU":"DR", "RD":"UL",
                                             "DR":"RU", "DL":"LD", "LD":"DL", "LU":"UR"})
