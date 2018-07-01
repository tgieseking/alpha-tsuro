from Piece import Piece
from Board import Board

class Player:
    def __init__(self, board, deck):
        self.board = board
        self.piece = Piece(board, 0, 0, "UL")
        self.hand = [deck.draw() for i in range(3)]

    def take_turn(self):
        selected_piece, index = self.select_piece()
        board.tiles[piece.col][piece.row] = selected_piece
        self.hand[index] = deck.draw()


    def select_piece(self):
        return 