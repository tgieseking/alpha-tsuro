from Piece import Piece
import random

class PlayerAgent:
    def __init__(self, board, deck, piece_row, piece_col, piece_position):
        self.board = board
        self.piece = Piece(board, piece_row, piece_col, piece_position)
        self.hand_size = 3
        self.hand = [deck.draw() for i in range(self.hand_size)]
        self.deck = deck

    def take_turn(self):
        selected_tile_index, num_rotations = self.select_tile()
        self.hand[selected_tile_index].rotate_clockwise(num_rotations)
        selected_tile = self.hand[selected_tile_index]
        self.board.tiles[self.piece.row][self.piece.col] = selected_tile
        if self.deck.isEmpty():
            del self.hand[selected_tile_index]
        else:
            self.hand[selected_tile_index] = self.deck.draw()


    def select_tile(self):
        """
            This will select a tile by returning a piece index and the number of clockwise rotations to make.
        """
        pass

    def is_human(self):
        return False

class RandomAgent(PlayerAgent):
    def select_tile(self):
        tile_index = random.randrange(0, len(self.hand))
        num_rotations = random.randrange(0, 4)
        print((tile_index, num_rotations))
        return (tile_index, num_rotations)
