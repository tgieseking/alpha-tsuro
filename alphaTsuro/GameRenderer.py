import pygame
import math

class GameRenderer:
    def __init__(self):
        self.SCALE_FACTOR = 4
        self.BACKGROUND_COLOR = (255, 255, 255)

        self.TILE_SIZE = 40 * self.SCALE_FACTOR
        self.TILE_MARK_DIST = 10 * self.SCALE_FACTOR # the distance from the corner to a path connection point
        self.TILE_BORDER_WIDTH = 2 * self.SCALE_FACTOR
        self.TILE_BORDER_COLOR = (0, 0, 0)
        self.TILE_PATH_WIDTH = 2 * self.SCALE_FACTOR
        self.TILE_PATH_COLOR = (127, 55, 0)

        self.BOARD_TOP_MARGIN = 40 * self.SCALE_FACTOR
        self.BOARD_BOTTOM_MARGIN = 40 * self.SCALE_FACTOR
        self.BOARD_SIDE_MARGIN = 40 * self.SCALE_FACTOR
        self.BOARD_LINE_WIDTH = 2 * self.SCALE_FACTOR
        self.BOARD_LINE_COLOR = (0, 0, 0)

        self.HAND_VERTICAL_MARGIN = 10 * self.SCALE_FACTOR
        self.HAND_HORIZONTAL_MARGIN = 20 * self.SCALE_FACTOR

        self.HAND_SELECTION_PADDING = 5 * self.SCALE_FACTOR
        self.HAND_SELECTION_LINE_COLOR = (255, 135, 40)
        self.HAND_SELECTION_LINE_WIDTH = 2 * self.SCALE_FACTOR

        self.PIECE_RADIUS = 5 * self.SCALE_FACTOR
        self.PIECE_COLORS = [(255, 0, 0), (0, 0, 255)]

        self.WIN_MESSAGE_COLOR = (0, 0, 0)
        self.WIN_MESSAGE_TOP_MARGIN = 100 * self.SCALE_FACTOR
        self.WIN_MESSAGE_PADDING = 5 * self.SCALE_FACTOR
        self.WIN_MESSAGE_BACKGROUND_COLOR = (255, 255, 255)
        self.WIN_MESSAGE_BORDER_COLOR = (0, 0, 0)
        self.WIN_MESSAGE_BORDER_WIDTH = 2 * self.SCALE_FACTOR
        self.WIN_MESSAGE_FONT_SIZE = 20 * self.SCALE_FACTOR

    def initialize_screen(self, game_state):
        self.screen_width = 2 * self.BOARD_SIDE_MARGIN + game_state.board.board_size * self.TILE_SIZE
        self.board_height = self.BOARD_TOP_MARGIN + game_state.board.board_size * self.TILE_SIZE + self.BOARD_BOTTOM_MARGIN
        self.player_hand_height = 2 * self.HAND_VERTICAL_MARGIN + self.TILE_SIZE
        self.screen_height = self.board_height + self.player_hand_height
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def render_game_state(self, game_state, ui_state = {}):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.render_board(game_state.board)
        self.render_pieces([player.piece for player in game_state.players])
        if "hand_selection" in ui_state:
            self.render_hand(ui_state["hand_selection"]["hand"])
            self.render_hand_selection(ui_state["hand_selection"])
        if "win_state" in ui_state:
            self.render_win_state(ui_state["win_state"])
        pygame.display.flip()

    def render_tile(self, tile, x, y):
        pygame.draw.rect(self.screen, self.TILE_BORDER_COLOR, [x, y, self.TILE_SIZE, self.TILE_SIZE], self.TILE_BORDER_WIDTH)
        # we subtract 1 from the far edges to get the path and border rendering to align
        point_coords = {"UL":[x + self.TILE_MARK_DIST, y],
                        "UR":[x + self.TILE_SIZE - self.TILE_MARK_DIST, y],
                        "RU":[x + self.TILE_SIZE - 1, y + self.TILE_MARK_DIST],
                        "RD":[x + self.TILE_SIZE - 1, y + self.TILE_SIZE - self.TILE_MARK_DIST],
                        "DR":[x + self.TILE_SIZE - self.TILE_MARK_DIST, y + self.TILE_SIZE - 1],
                        "DL":[x + self.TILE_MARK_DIST, y + self.TILE_SIZE - 1],
                        "LD":[x, y + self.TILE_SIZE - self.TILE_MARK_DIST],
                        "LU":[x, y + self.TILE_MARK_DIST]}
        for point in tile.connections:
            if point[0] == tile.connections[point][0]:
                # the endpoints are on the same edges
                width = self.TILE_SIZE - 2 * self.TILE_MARK_DIST
                if point[0] == "U":
                    pygame.draw.arc(self.screen, self.TILE_PATH_COLOR, [x + self.TILE_MARK_DIST, y - width // 2, width, width], math.radians(180), math.radians(360), self.TILE_PATH_WIDTH)
                elif point[0] == "D":
                    pygame.draw.arc(self.screen, self.TILE_PATH_COLOR, [x + self.TILE_MARK_DIST, y + self.TILE_SIZE - width // 2, width, width], math.radians(0), math.radians(180), self.TILE_PATH_WIDTH)
                elif point[0] == "L":
                    pygame.draw.arc(self.screen, self.TILE_PATH_COLOR, [x - width // 2, y + self.TILE_MARK_DIST, width, width], math.radians(270), math.radians(450), self.TILE_PATH_WIDTH)
                elif point[0] == "R":
                    pygame.draw.arc(self.screen, self.TILE_PATH_COLOR, [x + self.TILE_SIZE - width // 2, y + self.TILE_MARK_DIST, width, width], math.radians(90), math.radians(270), self.TILE_PATH_WIDTH)
            else:
                pygame.draw.line(self.screen, self.TILE_PATH_COLOR, point_coords[point], point_coords[tile.connections[point]], self.TILE_PATH_WIDTH)

    def render_board(self, board):
        for row in range(board.board_size):
            for col in range(board.board_size):
                x = self.BOARD_SIDE_MARGIN + col * self.TILE_SIZE
                y = self.BOARD_TOP_MARGIN + row * self.TILE_SIZE
                tile = board.tiles[row][col]
                if tile == None:
                    pygame.draw.rect(self.screen, self.BOARD_LINE_COLOR, [x, y, self.TILE_SIZE, self.TILE_SIZE], self.BOARD_LINE_WIDTH)
                else:
                    self.render_tile(tile, x, y)

    def render_pieces(self, pieces):
        for i, piece in enumerate(pieces):
            self.render_piece(piece, i)

    def render_piece(self, piece, piece_index):
        point_offsets = {"UL":[self.TILE_MARK_DIST, 0],
                         "UR":[self.TILE_SIZE - self.TILE_MARK_DIST, 0],
                         "RU":[self.TILE_SIZE - 1, self.TILE_MARK_DIST],
                         "RD":[self.TILE_SIZE - 1, self.TILE_SIZE - self.TILE_MARK_DIST],
                         "DR":[self.TILE_SIZE - self.TILE_MARK_DIST, self.TILE_SIZE - 1],
                         "DL":[self.TILE_MARK_DIST, self.TILE_SIZE - 1],
                         "LD":[0, self.TILE_SIZE - self.TILE_MARK_DIST],
                         "LU":[0, self.TILE_MARK_DIST]}
        x = self.BOARD_SIDE_MARGIN + piece.col * self.TILE_SIZE + point_offsets[piece.edge_position][0]
        y = self.BOARD_TOP_MARGIN + piece.row * self.TILE_SIZE + point_offsets[piece.edge_position][1]
        pygame.draw.circle(self.screen, self.PIECE_COLORS[piece_index], [x, y], self.PIECE_RADIUS)

    def render_hand(self, hand):
        total_hand_width = len(hand) * (self.TILE_SIZE + 2 * self.HAND_HORIZONTAL_MARGIN)
        for i, tile in enumerate(hand):
            tile_x = (self.screen_width - total_hand_width) // 2 + i * (2 * self.HAND_HORIZONTAL_MARGIN + self.TILE_SIZE) + self.HAND_HORIZONTAL_MARGIN
            tile_y = self.board_height + self.HAND_VERTICAL_MARGIN
            self.render_tile(tile, tile_x, tile_y)

    def render_hand_selection(self, hand_selection):
        hand_y = self.board_height
        y = self.board_height + self.HAND_VERTICAL_MARGIN - self.HAND_SELECTION_PADDING
        total_hand_width = len(hand_selection["hand"]) * (self.TILE_SIZE + 2 * self.HAND_HORIZONTAL_MARGIN)
        x = (self.screen_width - total_hand_width) // 2 + hand_selection["selected_tile"] * (2 * self.HAND_HORIZONTAL_MARGIN + self.TILE_SIZE) + self.HAND_HORIZONTAL_MARGIN - self.HAND_SELECTION_PADDING
        pygame.draw.rect(self.screen, self.PIECE_COLORS[hand_selection["player_index"]], [x, y, self.TILE_SIZE + 2 * self.HAND_SELECTION_PADDING, self.TILE_SIZE + 2 * self.HAND_SELECTION_PADDING], self.HAND_SELECTION_LINE_WIDTH)

    def render_win_state(self, win_state):
        WIN_MESSAGE_FONT = pygame.font.SysFont('Arial', self.WIN_MESSAGE_FONT_SIZE)
        if win_state["win_state"] == "win":
            message = "The winner is player " + str(win_state["winner"] + 1)
        elif win_state["win_state"] == "tie":
            message = "It's a draw"
        text_surface = WIN_MESSAGE_FONT.render(message, False, self.WIN_MESSAGE_COLOR)
        x = (self.screen_width - text_surface.get_width()) // 2
        pygame.draw.rect(self.screen, self.WIN_MESSAGE_BACKGROUND_COLOR, [x - self.WIN_MESSAGE_PADDING, self.WIN_MESSAGE_TOP_MARGIN - self.WIN_MESSAGE_PADDING, text_surface.get_width() + 2 * self.WIN_MESSAGE_PADDING, text_surface.get_height() + 2 * self.WIN_MESSAGE_PADDING])
        pygame.draw.rect(self.screen, self.WIN_MESSAGE_BORDER_COLOR, [x - self.WIN_MESSAGE_PADDING, self.WIN_MESSAGE_TOP_MARGIN - self.WIN_MESSAGE_PADDING, text_surface.get_width() + 2 * self.WIN_MESSAGE_PADDING, text_surface.get_height() + 2 * self.WIN_MESSAGE_PADDING], self.WIN_MESSAGE_BORDER_WIDTH)
        self.screen.blit(text_surface, (x, self.WIN_MESSAGE_TOP_MARGIN))
