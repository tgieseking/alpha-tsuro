from Board import Board
from Deck import Deck
from Player import Player

class GameState:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.players = [Player(self, self.board, self.deck, 0, 2, "UR"), Player(self, self.board, self.deck, 5, 3, "DL")]
