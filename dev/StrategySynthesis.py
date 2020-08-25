from __future__ import print_function
import logging
from tulip import spec
from tulip import synth
from tulip.transys import machines
from time import time
import yaml
import networkx as nx
from random import choice

logging.basicConfig(level=logging.ERROR)


# https://networkx.github.io/documentation/stable/reference/classes/multigraph.html
def time_wrap(func):
    def runtime(*args, **kwargs):
        tic = time()
        strategy = func(*args, **kwargs)
        toc = time()
        print(f"processing time is {toc - tic:.3f} sec")
        return strategy

    return runtime


@time_wrap
def strategy_synthesis(conf):
    # yaml file values are in list format, need to convert list to set

    for key in conf:
        if key == "out_file": continue
        # for new style of specification
        elif isinstance(conf['env_safe'], dict) or isinstance(conf['sys_safe'], dict):
            if (key == 'env_safe') or (key == 'sys_safe'):
                for i, k in enumerate(conf[key].values()):
                    if i == 0:
                        conf[key] = set(k)
                    else:
                        conf[key] |= set(k)
            else:
                conf[key] = set(conf[key])
        else: # for old style of specification
            conf[key] = set(conf[key])


    conf['sys_safe'].add(synth.exactly_one(
        conf['sys_vars']
    )[0])
    # Create the specification
    specs = spec.GRSpec(conf['env_vars'], conf['sys_vars'], conf['env_init'], conf['sys_init'],
                        conf['env_safe'], conf['sys_safe'], conf['env_prog'], conf['sys_prog'])
    # Controller synthesis using Moore machines
    specs.moore = True
    specs.qinit = '\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

    strategy = synth.synthesize(specs)
    assert strategy is not None, 'unrealizable'
    return strategy


def get_plans(G, x):
    # target -> a2
    for u, v, keys, weight in G.edges(data="a2", keys=True):
        if weight:
            yield nx.shortest_path(G, x, v)


@time_wrap
def show_random_plan(G, x):
    plans = list(get_plans(G, x))
    plan = choice(plans)
    print(plan)
    return plan


@time_wrap
def save_graph(G, name):
    print(name)
    nx.write_gpickle(G, "{}".format(name))


if __name__ == '__main__':
    with open('../param.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    GRID_SIZE = '3x3'
    print('> Synthesizing strategy for ', GRID_SIZE)
    startegy = strategy_synthesis(config[GRID_SIZE])
    print('> Executing strategy randomly')
    show_random_plan(G=startegy, x='Sinit')
    print("> writing graph")
    save_graph(startegy, config[GRID_SIZE])
