from __future__ import print_function
from time import time
from tulip import spec
from tulip import synth

#     +------+-----+------+
#     | 11(d)| ... | 1n   |
#     +------+-----+------+
#     |      |     |      |
#     +------+-----+------+
#     | m1(a)| ... | mn(t)|
#     +------+-----+------+

k = 5

m = k
n = k
a_init = [k, 1]
d_init = [1, 1]
t = [k, k]
obs = []  # list of obstacles


def sensor(player, i, j):
    return player + str(i) + str(j)


def singular(player, index, ind, n_row, n_col):
    sing_expr = sensor(player, index[0], index[1])
    for k in range(1, n_row+1):
        for l in range(1, n_col+1):
            if ([l, k] != index) and ([l, k] in ind):
                sing_expr += ' && !' + sensor(player, l, k)
    return sing_expr


def neighbors(index, ind, n_row, n_col):
    n = [(index[0]+a[0], index[1]+a[1])
         for a in [(-1, 0), (1, 0), (0, -1), (0, 1)]
         if ((1 <= index[0]+a[0] < n_row+1) and (1 <= index[1]+a[1] < n_col+1)
             and [index[0]+a[0], index[1]+a[1]] in ind)]
    return n


# Defender variables
env_ind = [[i, j] for i in range(1, m+1) for j in range(1, n+1)
           if [i, j] not in [t]+obs]


env_vars = set(
    [sensor('d', i, j)
     for i in range(1, m+1)
     for j in range(1, n+1)
     if [i, j] not in [t] + obs]
)

# Defender initial condition
env_init = {singular('d', d_init, env_ind, m, n)}

# Defender transitions (termination):
env_term = []
for i in range(1, m+1):
    for j in range(1, n+1):
        if [i, j] in env_ind:
            env_term.append(sensor('d', i, j) + ' && ' + sensor('a', i, j) +
                            ' -> X (' + singular('d', [i, j], env_ind, m, n) +
                            ')')
env_safe = set(env_term)

env_term = []
for i in range(1, m+1):
    for j in range(1, n+1):
        if [i, j] in env_ind:
            env_term.append(
                sensor('d', i, j) + ' && ' +
                sensor('a', t[0], t[1]) + ' -> X (' +
                singular('d', [i, j], env_ind, m, n) + ')')
env_safe |= set(env_term)

env_trans = []
for i in range(1, m+1):
    for j in range(1, n+1):
        if [i, j] in env_ind:
            neighbors_ij = neighbors([i, j], env_ind, m, n)
            s = sensor('d', i, j) + ' && ' + sensor('!a', i, j) + ' && ' + \
                sensor('!a', t[0], t[1]) + ' -> X ('
            num = 1
            for neighbor in neighbors_ij:
                s += '(' + singular('d', list(neighbor), env_ind, m, n) + ')'
                if num < len(neighbors_ij):
                    s += ' || '
                num += 1
            env_trans.append(s + ')')
env_safe |= set(env_trans)

# defender objective
env_prog = {'True'}

# System variables
sys_vars = set(
    [sensor('a', i, j) for i in range(1, m+1) for j in range(1, n+1)
     if [i, j] not in obs]
)

sys_ind = env_ind + [t]

# attacker initial condition
sys_init = {sensor('a', a_init[0], a_init[1])}


# attacker termination
sys_term = []
for i in range(1, m+1):
    for j in range(1, n+1):
        if [i, j] in env_ind:
            sys_term.append(sensor('a', i, j) + ' && ' + sensor('d', i, j) +
                            ' -> X ' + sensor('a', i, j))
sys_safe = set(sys_term)

sys_safe |= {sensor('a', t[0], t[1]) + ' -> X ' + sensor('a', t[0], t[1])}

sys_trans = []
for i in range(1, m+1):
    for j in range(1, n+1):
        if [i, j] in env_ind:
            neighbors_ij = neighbors([i, j], sys_ind, m, n)
            s = sensor('a', i, j) + ' && ' + sensor('!d', i, j) + ' -> X ('
            num = 1
            for neighbor in neighbors_ij:
                s += sensor('a', neighbor[0], neighbor[1])
                if num < len(neighbors_ij):
                    s += ' || '
                num += 1
            sys_trans.append(s + ')')


sys_safe |= set(sys_trans)

sys_safe.add(synth.exactly_one(set(
    [sensor('a', i, j) for i in range(1, m+1) for j in range(1, n+1)
     if [i, j] not in obs]
))[0])

sys_prog = {sensor('a', t[0], t[1])}

specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)
specs.moore = True
specs.qinit = '\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

tic = time()
strategy = synth.synthesize(specs)
toc = time()

if strategy is not None:
    print(toc-tic)
