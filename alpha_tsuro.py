from alphaTsuro.GameController import GameController
from alphaTsuro.SimulationController import SimulationController
from alphaTsuro.Agents import HumanAgent, AvoidDeathAgent, MCTSAgent
import argparse

def parse_agent(agent_args):
    agent_type = agent_args[0].lower()
    if agent_type == "human":
        return HumanAgent()
    elif agent_type == "greedy":
        return AvoidDeathAgent()
    elif agent_type == "mcts":
        if len(agent_args) > 1:
            num_iterations = int(agent_args[1])
        else:
            num_iterations = 100
        if len(agent_args) > 2:
            num_randomizations = int(agent_args[2])
        else:
            num_randomizations  = 10
        return MCTSAgent(num_iterations, num_randomizations)
    else:
        raise ValueError

parser = argparse.ArgumentParser()
parser.add_argument("--player1", "-p1", help="selects the agent for player one", nargs="+", default=["human"])
parser.add_argument("--player2", "-p2", help="selects the agent for player two", nargs="+", default=["human"])
parser.add_argument("--runs", "-r", help="the number runs if using the --nographics option", type=int, default=100)
parser.add_argument("--nographics", "-ng", help="turns off the graphics", action="store_true")
args = parser.parse_args()
player1 = parse_agent(args.player1)
player2 = parse_agent(args.player2)
agents = [player1, player2]
if args.nographics:
    if not agents[0].is_human() and not agents[1].is_human():
        SimulationController().run(agents, args.runs)
    else:
        print("In no graphics mode, no player can be human")
else:
    GameController().run(agents)
