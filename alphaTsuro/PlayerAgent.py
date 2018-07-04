from Piece import Piece
import random
import copy

class PlayerAgent:
    def __init__(self, index, game_state, piece_row, piece_col, piece_position):
        self.game_state = game_state
        self.board = game_state.board
        self.piece = Piece(game_state.board, piece_row, piece_col, piece_position)
        self.hand_size = 3
        self.hand = [game_state.deck.draw() for i in range(self.hand_size)]
        self.deck = game_state.deck
        self.index = index

    def take_turn(self):
        selected_tile_index, num_rotations = self.select_tile()
        self.hand[selected_tile_index].rotate_clockwise(num_rotations)
        selected_tile = self.hand[selected_tile_index]
        self.board.tiles[self.piece.row][self.piece.col] = selected_tile
        if self.deck.isEmpty():
            del self.hand[selected_tile_index]
        else:
            self.hand[selected_tile_index] = self.deck.draw()


    def select_tile(self):
        """
            This will select a tile by returning a piece index and the number of clockwise rotations to make.
        """
        pass

    def is_human(self):
        return False

    def get_next_state(self, selected_tile_index, num_rotations):
        game_state_copy = copy.deepcopy(self.game_state)
        agent_copy = game_state_copy.players[self.index]
        selected_tile = agent_copy.hand[selected_tile_index]
        selected_tile.rotate_clockwise(num_rotations)
        game_state_copy.board.tiles[agent_copy.piece.row][agent_copy.piece.col] = selected_tile
        game_state_copy.update_pieces()
        return game_state_copy


class RandomAgent(PlayerAgent):
    def select_tile(self):
        tile_index = random.randrange(0, len(self.hand))
        num_rotations = random.randrange(0, 4)
        print((tile_index, num_rotations))
        return (tile_index, num_rotations)

class AvoidDeathAgent(PlayerAgent):
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
