from .Piece import Piece
import random
import copy
from .MCTS import GameTree, UCBSelector

class HumanAgent:
    def is_human(self):
        return True

class ComputerAgent:
    def is_human(self):
        return False

class RandomAgent(ComputerAgent):
    def select_tile(self, game_state):
        hand_size = len(game_state.players[game_state.current_player_index].hand)
        tile_index = random.randrange(0, hand_size)
        num_rotations = random.randrange(0, 4)
        return (tile_index, num_rotations)

class AvoidDeathAgent(ComputerAgent):
    def __init__(self):
        self.copies = 0

    def select_tile(self, game_state):
        player_index = game_state.current_player_index
        hand_size = len(game_state.players[game_state.current_player_index].hand)
        wins = []
        ongoings = []
        ties = []
        losses = []
        for tile_index in range(hand_size):
            for num_rotations in range(4):
                next_state = game_state.take_turn_copy(tile_index, num_rotations)
                self.copies += 1
                win_state = next_state.check_win_state()
                if win_state["win_state"] == "win":
                    if win_state["winner"] == player_index:
                        wins.append((tile_index, num_rotations))
                    else:
                        losses.append((tile_index, num_rotations))
                elif win_state["win_state"] == "tie":
                    ties.append((tile_index, num_rotations))
                elif win_state["win_state"] == "ongoing":
                    ongoings.append((tile_index, num_rotations))
                else:
                    raise InvalidWinStateException()
        if len(wins) > 0:
            return wins[0]
        if len(ongoings) > 0:
            return ongoings[0]
        if len(ties) > 0:
            return ties[0]
        else:
            return losses[0]

class MCTSAgent(ComputerAgent):
    def __init__(self, num_iterations = 100, num_randomizations = 10):
        self.num_randomizations = num_randomizations
        self.num_iterations = num_iterations

    def select_tile(self, game_state):
        # import pdb; pdb.set_trace()
        total_value = {}
        visits = {}
        player_index = game_state.current_player_index
        for action in game_state.possible_actions():
            total_value[action] = 0
            visits[action] = 0
        for i in range(self.num_randomizations):
            # print("Starting randomization " + str(i))
            root_state = game_state.get_randomization(player_index)
            game_tree = GameTree(root_state)
            for j in range(self.num_iterations):
                # print("starting iteration " + str(j))
                game_tree.simulate_game(UCBSelector)
            for action in total_value:
                action_node = game_tree.root.children[action]
                total_value[action] += action_node.total_value[player_index]
                visits[action] += action_node.visits
        best_action = None
        best_value = None
        for action in total_value:
            average_value = total_value[action] / visits[action]
            if not best_value or best_value < average_value:
                best_value = average_value
                best_action = action
        return best_action

class InvalidWinStateException(Exception):
    pass
