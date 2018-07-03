from Piece import Piece
from Board import Board

class Player:
    def __init__(self, board, deck, piece_row, piece_col, piece_position):
        self.board = board
        self.piece = Piece(board, piece_row, piece_col, piece_position)
        self.hand_size = 3
        self.hand = [deck.draw() for i in range(self.hand_size)]
        self.deck = deck

    def select_tile(self, selected_tile_index):
        selected_tile = self.hand[selected_tile_index]
        self.board.tiles[self.piece.row][self.piece.col] = selected_tile
        if self.deck.isEmpty():
            del self.hand[selected_tile_index]
        else:
            self.hand[selected_tile_index] = self.deck.draw()
