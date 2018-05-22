import pygame

LEFT_MARGIN = 40
TOP_MARGIN = 40
GRID_SIZE = 40
GRID_WIDTH = 2

class Board:
    """The game board."""
    def __init__(self):
        self.board_size = 8
        self.tiles = [[None for i in range(self.board_size)] for j in range(self.board_size)]

    def draw(self, screen):
        BLACK = (  0,   0,   0)
        for i in range(8):
            for j in range(8):
                x = LEFT_MARGIN + i * GRID_SIZE
                y = TOP_MARGIN + j * GRID_SIZE
                pygame.draw.rect(screen, BLACK, [x, y, GRID_SIZE, GRID_SIZE], GRID_WIDTH)

