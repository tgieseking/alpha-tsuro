from GameState import GameState
import Agents
import copy
import time

class SimulationController:
    def run(self, num_games, agents=[Agents.AvoidDeathAgent(), Agents.AvoidDeathAgent()]):
        num_games
        points = [0, 0]
        start = time.time()

        for i in range(num_games):
            game_state = GameState()
            win_state = {"win_state": "ongoing"}
            while win_state["win_state"] == "ongoing":
                current_agent = agents[game_state.current_player_index]
                tile_index, num_rotations = current_agent.select_tile(game_state)
                game_state.take_turn(tile_index, num_rotations)
                win_state = game_state.check_win_state()
            if win_state["win_state"] == "tie":
                points[0] += 1
                points[1] += 1
            elif win_state["win_state"] == "win":
                points[win_state["winner"]] += 2

        print("time = " + str(time.time() - start))
        print("copies = " + str(agents[0].copies + agents[1].copies))
        print(points)
