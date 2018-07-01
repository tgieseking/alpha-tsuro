from Board import Board
from Deck import Deck
from Player import Player

class GameState:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.players = [Player(self.board, self.deck), Player(self.board, self.deck)]
