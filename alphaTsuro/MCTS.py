import random
import math

class GameTree:
    def __init__(self, root_state):
        self.root_state = root_state
        self.root = GameNode()

    def simulate_game(self, selection_alg):
        game_state = copy.deepcopy(self.root_state)
        leaf = self.select(selection_alg)
        player_rewards = self.random_playout(game_state)
        self.backpropogate(leaf, player_rewards)

    def select(self, selection_alg, game_state):
        current_node = self.root
        while True:
            possible_actions = game_state.possible_actions()
            if len(possible_actions) == 0:
                return current_node
            selected_action = selection_alg(current_node, possible_actions, game_state.current_player_index)
            game_state.take_action(selected_action)
            if selected_action in current_node.children:
                current_node = current_node.children[selected_action]
            else:
                new_node = GameNode(current_node)
                current_node.children[selected_action] = new_node
                return new_node

    def random_playout(self, game_state):
        while True:
            possible_actions = game_state.possible_actions()
            if len(possible_actions) == 0:
                return game_state.player_rewards()
            selected_action = random.choice(possible_actions)
            game_state.take_action(selected_action)

    def backpropogate(self, leaf, player_rewards):
        current_node = leaf
        while current_node != None:
            current_node.visits += 1
            for i in range(len(player_rewards)):
                current_node.total_value[i] += player_rewards[i]

class GameNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}
        self.total_value = [0,0]
        self.visits = 0

def UCBSelector(node, possible_actions, current_player_index):
    best_action = None
    max_ucb = None
    for action in possible_actions:
        if not action in node.children:
            return action
        else:
            ucb = (node.children[action].total_value[current_player_index] / node.children[action].visits) + UCB_CONST * math.sqrt(math.log(node.visits) / math.log(node.children[action].visits))
            if not best_action or ucb > max_ucb:
                best_action = action
                max_ucb = ucb
