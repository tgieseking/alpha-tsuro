class Board:
    """The game board."""
    def __init__(self):
        self.board_size = 8
        self.tiles = [[None for i in range(self.board_size)] for j in range(self.board_size)]

