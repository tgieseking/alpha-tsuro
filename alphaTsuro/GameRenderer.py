import pygame

class GameRenderer:
    def __init__(self):
        self.BACKGROUND_COLOR = (255, 255, 255)

        self.BOARD_TOP_MARGIN = 40
        self.BOARD_SIDE_MARGIN = 40
        self.BOARD_GRID_SIZE = 40
        self.BOARD_LINE_WIDTH = 2
        self.BOARD_LINE_COLOR = (0, 0, 0)

    def initialize_screen(self, game_state):
        pygame.init()
        screen_width = 2 * self.BOARD_SIDE_MARGIN + game_state.board.board_size * self.BOARD_GRID_SIZE
        screen_height = 400
        self.screen = pygame.display.set_mode([screen_width, screen_height])

    def render_game_state(self, game_state):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.render_board(game_state.board)
        pygame.display.flip()

    def render_board(self, board):
        for i in range(board.board_size):
            for j in range(board.board_size):
                x = self.BOARD_SIDE_MARGIN + i * self.BOARD_GRID_SIZE
                y = self.BOARD_TOP_MARGIN + j * self.BOARD_GRID_SIZE
                pygame.draw.rect(self.screen, self.BOARD_LINE_COLOR, [x, y, self.BOARD_GRID_SIZE, self.BOARD_GRID_SIZE], self.BOARD_LINE_WIDTH)
