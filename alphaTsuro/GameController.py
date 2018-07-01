import pygame
from GameRenderer import GameRenderer
from GameState import GameState

class GameController:
    def __init__(self):
        self.game_renderer = GameRenderer()
        self.game_state = GameState()
        self.state = InitializeState(self, self.game_state, self.game_renderer)
        self.game_loop()

    def game_loop(self):
        #Loop until the user clicks the close button.
        done = False
        clock = pygame.time.Clock()

        while not done:

            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            clock.tick(10)

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
                else:
                    self.state.handle_event(event, self.game_state)

class InitializeState:
    def __init__(self, game_controller, game_state, game_renderer):
        game_renderer.initialize_screen(game_state)
        game_renderer.render_game_state(game_state)

    def handle_event(self, event, game_state):
        return False
