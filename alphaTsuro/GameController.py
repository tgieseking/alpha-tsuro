import pygame
from GameRenderer import GameRenderer
from GameState import GameState
from Agents import HumanAgent
import copy

class GameController:
    def __init__(self):
        self.game_renderer = GameRenderer()
        self.game_state = GameState()
        self.agents = [HumanAgent(), HumanAgent()]
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
        pygame.init()
        pygame.font.init()
        game_controller.game_renderer.initialize_screen(game_state)
        first_agent = game_controller.agents[0]
        if first_agent.is_human():
            game_controller.set_state(HumanTurnState(first_agent))
        else:
            game_controller.set_state(AgentTurnState(first_agent))

class NewGameState:
    def initialize(self, game_state, game_controller):
        new_game =  GameState()
        game_controller.game_state = new_game
        next_agent = game_controller.agents[0]
        if next_agent.is_human():
            game_controller.set_state(HumanTurnState(next_agent))
        else:
            game_controller.set_state(AgentTurnState(next_agent))

class HumanTurnState:
    def __init__(self, agent):
        self.selected_tile = 0

    def initialize(self, game_state, game_controller):
        self.player_index = game_state.current_player_index
        self.hand = copy.deepcopy(game_state.players[self.player_index].hand)
        self.hand_size = len(self.hand)
        self.rotations = [0] * self.hand_size

    def handle_event(self, event, game_state, game_controller):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_tile = max(self.selected_tile - 1, 0)
                return True
            if event.key == pygame.K_RIGHT:
                self.selected_tile = min(self.selected_tile + 1, self.hand_size - 1)
                return True
            if event.key == pygame.K_UP:
                self.hand[self.selected_tile].rotate_clockwise()
                self.rotations[self.selected_tile] = (self.rotations[self.selected_tile] + 1) % 4
                return True
            if event.key == pygame.K_DOWN:
                self.hand[self.selected_tile].rotate_clockwise(-1)
                self.rotations[self.selected_tile] = (self.rotations[self.selected_tile] - 1) % 4
                return True
            if event.key == pygame.K_RETURN:
                game_state.take_turn(self.selected_tile, self.rotations[self.selected_tile])
                win_state = game_state.check_win_state()
                if win_state["win_state"] == "ongoing":
                    next_agent = game_controller.agents[game_state.current_player_index]
                    if next_agent.is_human():
                        game_controller.set_state(HumanTurnState(next_agent))
                    else:
                        game_controller.set_state(AgentTurnState(next_agent))
                else:
                    game_controller.set_state(GameEndState(win_state))
                return True
        return False

    def get_ui_state(self):
        return {"hand_selection":{"hand": self.hand, "player_index":self.player_index, "selected_tile":self.selected_tile}}

class AgentTurnState:
    def __init__(self, agent):
        self.agent = agent

    def initialize(self, game_state, game_controller):
        tile_index, num_rotations = self.agent.select_tile(game_state)
        game_state.take_turn(tile_index, game_state)
        win_state = game_state.check_win_state()
        if win_state["win_state"] == "ongoing":
            next_agent = game_controller.agents[game_state.current_player_index]
            if next_agent.is_human():
                game_controller.set_state(HumanTurnState(next_agent))
            else:
                game_controller.set_state(AgentTurnState(next_agent))
        else:
            game_controller.set_state(GameEndState(win_state))

    def get_ui_state(self):
        return {}

class GameEndState:
    def __init__(self, win_state):
        self.win_state = win_state

    def initialize(self, game_state, game_controller):
        return

    def handle_event(self, event, game_state, game_controller):
        if event.type == pygame.KEYDOWN:
            game_controller.set_state(NewGameState())

    def get_ui_state(self):
        return {"win_state": self.win_state}
