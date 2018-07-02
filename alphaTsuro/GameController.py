import pygame
from GameRenderer import GameRenderer
from GameState import GameState

class GameController:
    def __init__(self):
        self.game_renderer = GameRenderer()
        self.game_state = GameState()
        self.set_state(InitializeState())
        self.game_loop()

    def set_state(self, state):
        self.state = state
        self.state.initialize(self.game_state, self)
        self.game_renderer.render_game_state(self.game_state, self.state.get_ui_state())

    def game_loop(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(10)

            need_rerender = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=True
                else:
                    need_rerender = need_rerender or self.state.handle_event(event, self.game_state, self)

            if (need_rerender):
                self.game_renderer.render_game_state(self.game_state, self.state.get_ui_state())

class InitializeState:
    def initialize(self, game_state, game_controller):
        game_controller.game_renderer.initialize_screen(game_state)
        game_controller.set_state(PlayerTurnState(game_state.players[0], 0))

    def handle_event(self, event, game_state, game_controller):
        return False

    def get_ui_state(self):
        return {}

class PlayerTurnState:
    def __init__(self, player, player_index):
        self.player = player
        self.player_index = player_index
        self.selected_tile = 0
        self.hand_size = len(player.hand)

    def initialize(self, game_state, game_controller):
        return

    def handle_event(self, event, game_state, game_controller):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_tile = max(self.selected_tile - 1, 0)
                return True
            if event.key == pygame.K_RIGHT:
                self.selected_tile = min(self.selected_tile + 1, self.hand_size - 1)
                return True
            if event.key == pygame.K_UP:
                self.player.hand[self.selected_tile].rotate_clockwise()
                return True
            if event.key == pygame.K_DOWN:
                self.player.hand[self.selected_tile].rotate_clockwise(-1)
                return True
            if event.key == pygame.K_RETURN:
                self.player.select_tile(self.selected_tile)
                next_player_index = (self.player_index + 1) % len(game_state.players)
                game_controller.set_state(PlayerTurnState(game_state.players[next_player_index], next_player_index))
                return True
        return False

    def get_ui_state(self):
        return {"hand_selection":{"player": self.player, "player_index":self.player_index, "selected_tile":self.selected_tile}}
