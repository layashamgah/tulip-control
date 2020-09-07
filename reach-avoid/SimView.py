import matplotlib.pyplot as plt
import networkx as nx
import yaml
from .StrategySynthesis import show_random_plan


def viz_strategy(conf):
    G = nx.read_yaml(conf['out_file'])
    plan = show_random_plan(G=G, x='Sinit')

if __name__ == '__main__':
    GRID_SIZE = '3x3'
    with open('param.yaml') as file:
        config = yaml.load(file, Loader=yaml.Loader)
    viz_strategy(config[GRID_SIZE])