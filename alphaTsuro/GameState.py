from .Board import Board
from .Deck import Deck
from .Player import Player
from .Agents import RandomAgent, AvoidDeathAgent
import copy

class GameState:
    def __init__(self):
        self.board = Board()
        self.deck = Deck.from_json("data/testDeck.json")
        self.deck.shuffle()
        self.players = [Player(0, self.board, self.deck, 0, 2, "UR"), Player(1, self.board, self.deck, 5, 3, "DL")]
        self.current_player_index = 0

    def possible_actions(self):
        win_state = self.check_win_state()
        if win_state["win_state"] == "ongoing":
            return [(tile_index, num_rotations) for tile_index in range(len(self.players[self.current_player_index].hand)) for num_rotations in range(4)]
        else:
            return []

    def take_action(self, action):
        selected_tile_index, num_rotations = action
        self.take_turn(selected_tile_index, num_rotations)

    def player_rewards(self):
        win_state = self.check_win_state()
        if win_state["win_state"] == "tie":
            return [0.5 for i in range(len(self.players))]
        elif win_state["win_state"] == "win":
            rewards = [0 for i in range(len(self.players))]
            rewards[win_state["winner"]] = 1
            return rewards

    def get_randomization(self, player_index):
        randomization = copy.deepcopy(self)
        other_player = randomization.players[1 - player_index]
        hand_size = len(other_player.hand)
        for i in range(hand_size):
            randomization.deck.tiles.append(other_player.hand.pop())
        randomization.deck.shuffle()
        for i in range(hand_size):
            other_player.hand.append(randomization.deck.draw())
        return randomization

    def take_turn_copy(self, selected_tile_index, num_rotations):
        new_state = copy.deepcopy(self)
        new_state.take_turn(selected_tile_index, num_rotations)
        return new_state

    def take_turn(self, selected_tile_index, num_rotations):
        self.players[self.current_player_index].take_turn(selected_tile_index, num_rotations)
        self.update_pieces();
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def update_pieces(self):
        for player in self.players:
            player.piece.update_position()

    def check_win_state(self):
        all_tiles_gone = True
        for player in self.players:
            if len(player.hand) > 0:
                all_tiles_gone = False
        if all_tiles_gone:
            return {"win_state": "tie"}

        not_elimated = []
        for i in range(len(self.players)):
            if self.players[i].piece.on_board():
                not_elimated.append(i)
        if len(not_elimated) == 0:
            return {"win_state": "tie"}
        if len(not_elimated) == 1:
            return {"win_state": "win", "winner": not_elimated[0]}
        return {"win_state": "ongoing"}
