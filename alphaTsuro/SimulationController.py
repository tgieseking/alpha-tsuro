from .GameState import GameState
from .Agents import AvoidDeathAgent, MCTSAgent
import copy
import time

class SimulationController:
    def run(self, agents, num_games):
        num_games
        points = [0, 0]
        start = time.time()

        for i in range(num_games):
            print("Starting game " + str(i))
            print("Score is " + str(points))
            agents.reverse()
            points.reverse()
            game_state = GameState()
            win_state = {"win_state": "ongoing"}
            while win_state["win_state"] == "ongoing":
                current_agent = agents[game_state.current_player_index]
                tile_index, num_rotations = current_agent.select_tile(game_state)
                game_state.take_turn(tile_index, num_rotations)
                win_state = game_state.check_win_state()
            if win_state["win_state"] == "tie":
                points[0] += 0.5
                points[1] += 0.5
            elif win_state["win_state"] == "win":
                points[win_state["winner"]] += 1

        print("time = " + str(time.time() - start))
        print(points)
