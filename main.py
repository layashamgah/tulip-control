import yaml
import networkx as nx
from dev import *
from copy import deepcopy
import os
current_dir = os.path.dirname(__file__)



def synthesis():
    print('> Synthesizing strategy for ', GRID_SIZE)
    startegy = strategy_synthesis(deepcopy(config[GRID_SIZE]))
    print('> Executing strategy randomly')
    show_random_plan(G=startegy, x='Sinit')
    print("> writing graph")
    save_graph(startegy, out_file)
def simulate_strategy():
    G = nx.read_gpickle(out_file)
    plan = show_random_plan(G=G, x='Sinit')
    show_animation = SimView(config[GRID_SIZE])
    viz_data = viz_strategy(config[GRID_SIZE], G, plan)
    show_animation(viz_data)

if __name__ == '__main__':
    param_file = os.path.join(current_dir, 'dev', 'param.yaml')
    print(param_file)
    with open(param_file, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    GRID_SIZE = '3x3'
    out_file = os.path.join(current_dir, 'dev', config[GRID_SIZE]['out_file'])
    synthesis()
    # simulate_strategy()
