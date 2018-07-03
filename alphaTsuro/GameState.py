from Board import Board
from Deck import Deck
from Player import Player

class GameState:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.players = [Player(self, self.board, self.deck, 0, 2, "UR"), Player(self, self.board, self.deck, 5, 3, "DL")]

    def update_pieces(self):
        for player in self.players:
            player.piece.update_position()

    def check_win_state(self):
        not_elimated = []
        for i in range(len(self.players)):
            if self.players[i].piece.on_board():
                not_elimated.append("player " + str(i + 1))
        if len(not_elimated) == 0:
            return {"win_state": "tie"}
        if len(not_elimated) == 1:
            return {"win_state": "win", "winner": not_elimated[0]}
        return {"win_state": "ongoing"}
