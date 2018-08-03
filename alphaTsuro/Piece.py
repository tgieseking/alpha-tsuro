from .Board import Board

class Piece:
    """A game piece"""
    def __init__(self, board, row, col, edge_position):
        if row < 0 or row >= board.board_size:
            raise InvalidPositionException
        if col < 0 or col >= board.board_size:
            raise InvalidPositionException
        if not edge_position in {"UL", "UR", "RU", "RD",
                                 "DR", "DL", "LD","LU"}:
            raise InvalidPositionException

        self.board = board
        self.row = row
        self.col = col
        self.edge_position = edge_position

    def on_board(self):
        return (self.row >= 0 and self.row < self.board.board_size and
                self.col >= 0 and self.col < self.board.board_size)

    def update_position(self):
        position_adjustment_dict = {
            "UL":(0,-1,"DL"),
            "UR":(0,-1,"DR"),
            "RU":(1,0,"LU"),
            "RD":(1,0,"LD"),
            "DR":(0,1,"UR"),
            "DL":(0,1,"UL"),
            "LD":(-1,0,"RD"),
            "LU":(-1,0,"RU")
        }
        while self.on_board() and self.board.tiles[self.row][self.col] != None:
            endpoint = self.board.tiles[self.row][self.col].connections[self.edge_position]
            position_adjustment = position_adjustment_dict[endpoint]
            self.col += position_adjustment[0]
            self.row += position_adjustment[1]
            self.edge_position = position_adjustment[2]


class InvalidPositionException(Exception):
    """Thrown when a game piece is initialized to a position outsize the game board"""
    pass
