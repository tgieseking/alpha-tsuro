from Board import Board
from Deck import Deck
from Player import Player
from PlayerAgent import RandomAgent, AvoidDeathAgent

class GameState:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.deck.shuffle()
        self.players = [Player(0, self.board, self.deck, 0, 2, "UR"), AvoidDeathAgent(1, self, 5, 3, "DL")]
        self.humans = [player for player in self.players if player.is_human()]

    def update_pieces(self):
        for player in self.players:
            player.piece.update_position()

    def check_win_state(self):
        not_elimated = []
        for i in range(len(self.players)):
            if self.players[i].piece.on_board():
                not_elimated.append(i)
        if len(not_elimated) == 0:
            return {"win_state": "tie"}
        if len(not_elimated) == 1:
            return {"win_state": "win", "winner": not_elimated[0]}
        return {"win_state": "ongoing"}
