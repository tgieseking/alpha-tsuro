from .Piece import Piece
import random
import copy

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

class InvalidWinStateException(Exception):
    pass
