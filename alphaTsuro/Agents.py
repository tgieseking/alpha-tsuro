from Piece import Piece
import random
import copy

class HumanAgent:
    def is_human(self):
        return True


class RandomAgent:
    def select_tile(self, game_state):
        tile_index = random.randrange(0, len(self.hand))
        num_rotations = random.randrange(0, 4)
        return (tile_index, num_rotations)

class AvoidDeathAgent:
    def select_tile(self):
        wins = []
        ongoings = []
        ties = []
        losses = []
        for tile_index in range(len(self.hand)):
            for num_rotations in range(4):
                next_state = self.get_next_state(tile_index, num_rotations)
                win_state = next_state.check_win_state()
                if win_state["win_state"] == "win":
                    if win_state["winner"] == self.index:
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
