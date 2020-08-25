import matplotlib.pyplot as plt
import yaml
import re
from math import floor
import numpy as np
from matplotlib.patches import Rectangle





class SimView:
    def __init__(self, conf):
        self.conf = conf
        self.grid_size = conf['grid_size']
        self.major_ticks = np.arange((self.grid_size[0]))
        self.minor_ticks = np.arange(self.grid_size[1])
        self.get_target(conf)

    def get_target(self, conf):
        k = conf['sys_prog'][0]
        _ind = int(re.sub(r"\D", "", k)[0])
        self.__target_coord = index2sub(_ind, self.grid_size)


    def __background(self):
        plt.clf()
        plt.grid(True, color='k', linestyle='-', linewidth=2)
        plt.axis([0, self.grid_size[0], 0, self.grid_size[1]])
        ax = plt.gca()
        target = Rectangle(self.__target_coord, 1, 1, alpha=0.5)
        ax.add_patch(target)
        ax.set_xticks(self.major_ticks)
        ax.set_xticks(self.minor_ticks, minor=True)
        ax.set_yticks(self.major_ticks)
        ax.set_yticks(self.minor_ticks, minor=True)
    def __call__(self, viz_data):
        for a, d in viz_data:
            self.__background()
            plt.scatter(a[0] + 0.5, a[1] + 0.5,  200 )
            plt.scatter(d[0] + 0.5, d[1] + 0.5,  200 )
            plt.pause(1.5)
        plt.show()


def index2sub(ind, arr):
    #     +-----+----+-----+
    #     | 6(d)| 7  | 8   |
    #     +-----+----+-----+
    #     | 3   | 4  | 5   |
    #     +-----+----+-----+
    #     | 0(a)| 1  | 2(t)|
    #     +-----+----+-----+
    rows = (ind % arr[1])
    cols = (ind / arr[1])
    return (floor(rows), floor(cols))


def viz_strategy(conf, G,  plan):
    # https://networkx.github.io/documentation/stable/reference/classes/multigraph.html

    arr_shape = conf['grid_size']
    attacker_state, defender_state = [], []
    for p in plan:
        for nbr, keydict in G[p].items():
            for i, (key, eattr) in enumerate(keydict.items()):
                attacker , defender = False, False
                for k in eattr:
                    _ind = int(re.sub(r"\D", "", k)[0])
                    _coord = index2sub(_ind, arr_shape)
                    if (k.startswith('a')):
                        v = eattr[k]
                        if v:
                            print("> [state: {}] {}{}".format(p, k, _coord), end= ' -> ')
                            attacker = True

                            attacker_state.append(_coord)
                    elif (k.startswith('d')):
                        v = eattr[k]
                        if v:
                            print("{}{}".format(k, _coord))
                            defender = True
                            defender_state.append(_coord)
                    if(attacker and defender):
                        break
                break
            break
    return zip(attacker_state, defender_state)



if __name__ == '__main__':
    GRID_SIZE = '3x3'
    with open('../param.yaml') as file:
        config = yaml.load(file, Loader=yaml.Loader)
    show_animation = SimView(config[GRID_SIZE])
    viz_data = SimView(config[GRID_SIZE])
    show_animation(viz_data)



    # write_pkl(G, GRID_SIZE)