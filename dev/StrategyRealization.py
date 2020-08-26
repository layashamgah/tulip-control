import networkx as nx
from collections import defaultdict
from pprint import pprint
def get_pairs(G):
    """
    The winning states (all the states in the strategy),
    pairs of (a, d) for a fixed d position.
    """
    output = defaultdict(list)
    for n, nbrsdict in G.adjacency():
        for nbr, keydict in nbrsdict.items():
            for key, eattr in keydict.items():
                result = [key for key in eattr if eattr[key]]
                # print(result)
                output[result[0]].append(list(reversed(result)))
    return output

'''
A function “next_state”  that gets the current state, a and d, and 
returns an attacker next position a’
'''
class NextStep:
    def __init__(self, G):
        self.G = G
        self.__reaction = self.__decode(G)
    def __call__(self, *args, **kwargs):
        # refer to 'tulip.transys.machines.MealyMachine.reaction'
        return self.__reaction(*args, **kwargs)
    @staticmethod
    def __decode(G):
        print(type(G.transitions.graph))
        return G.transitions.graph.reaction


if __name__ == '__main__':
    out_file = 'results/3x3_strategy.pkl'
    G = nx.read_gpickle(out_file)
    print(get_pairs(G))
    move = NextStep(G)
    # get next state
    # output = move(...)

