import pygame

class GameRenderer:
    def __init__(self):
        self.BACKGROUND_COLOR = (255, 255, 255)

        self.TILE_SIZE = 40
        self.TILE_MARK_DIST = 10 # the distance from the corner to a path connection point
        self.TILE_BORDER_WIDTH = 2
        self.TILE_BORDER_COLOR = (0, 0, 0)
        self.TILE_PATH_WIDTH = 2
        self.TILE_PATH_COLOR = (0, 255, 0)

        self.BOARD_TOP_MARGIN = 40
        self.BOARD_BOTTOM_MARGIN = 40
        self.BOARD_SIDE_MARGIN = 40
        self.BOARD_LINE_WIDTH = 2
        self.BOARD_LINE_COLOR = (0, 0, 0)

        self.HAND_VERTICAL_MARGIN = 10
        self.HAND_HORIZONTAL_MARGIN = 40

        self.PIECE_RADIUS = 5
        self.PIECE_COLORS = [(255, 0, 0), (0, 0, 255)]

    def initialize_screen(self, game_state):
        pygame.init()
        self.screen_width = 2 * self.BOARD_SIDE_MARGIN + game_state.board.board_size * self.TILE_SIZE
        self.board_height = self.BOARD_TOP_MARGIN + game_state.board.board_size * self.TILE_SIZE + self.BOARD_BOTTOM_MARGIN
        self.player_hand_height = 2 * self.HAND_VERTICAL_MARGIN + self.TILE_SIZE
        self.screen_height = self.board_height + len(game_state.players) * self.player_hand_height
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def render_game_state(self, game_state):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.render_board(game_state.board)
        self.render_pieces([player.piece for player in game_state.players])
        self.render_player_hands(game_state)
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
            pygame.draw.line(self.screen, self.TILE_PATH_COLOR, point_coords[point], point_coords[tile.connections[point]], self.TILE_PATH_WIDTH)

    def render_board(self, board):
        for i in range(board.board_size):
            for j in range(board.board_size):
                x = self.BOARD_SIDE_MARGIN + i * self.TILE_SIZE
                y = self.BOARD_TOP_MARGIN + j * self.TILE_SIZE
                pygame.draw.rect(self.screen, self.BOARD_LINE_COLOR, [x, y, self.TILE_SIZE, self.TILE_SIZE], self.BOARD_LINE_WIDTH)

    def render_player_hands(self, game_state):
        for i, player in enumerate(game_state.players):
            self.render_player_hand(player, self.board_height + i * self.player_hand_height)

    def render_player_hand(self, player, y):
        total_hand_width = len(player.hand) * (self.TILE_SIZE + 2 * self.HAND_HORIZONTAL_MARGIN)
        for i, tile in enumerate(player.hand):
            tile_x = (self.screen_width - total_hand_width) // 2 + i * (2 * self.HAND_HORIZONTAL_MARGIN + self.TILE_SIZE) + self.HAND_HORIZONTAL_MARGIN
            tile_y = y + self.HAND_VERTICAL_MARGIN
            self.render_tile(tile, tile_x, tile_y)

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
