from __future__ import print_function
from time import time
from tulip import spec
from tulip import synth
from tulip.transys import machines

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
logging.getLogger('tulip.interfaces.gr1c').setLevel(logging.DEBUG)

#     +-----+----+-----+
#     | 6(d)| 7  | 8   |
#     +-----+----+-----+
#     | 3   | 4  | 5   |
#     +-----+----+-----+
#     | 0(a)| 1  | 2(t)|
#     +-----+----+-----+

# Environment variables and specification
env_vars = {'d0', 'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'}
env_init = {'d6 && !d0 && !d1 && !d3 && !d4 && !d5 && !d7 && !d8'}

# Defender Transition rules:

env_safe = {
    '(d0 && a0) -> X d0',
    '(d1 && a1) -> X d1',
    '(d3 && a3) -> X d3',
    '(d4 && a4) -> X d4',
    '(d5 && a5) -> X d5',
    '(d6 && a6) -> X d6',
    '(d7 && a7) -> X d7',
    '(d8 && a8) -> X d8',
}
# termination (attacker wins):
env_safe |= {
    '(d0 && a2) -> X d0',
    '(d1 && a2) -> X d1',
    '(d3 && a2) -> X d3',
    '(d4 && a2) -> X d4',
    '(d5 && a2) -> X d5',
    '(d6 && a2) -> X d6',
    '(d7 && a2) -> X d7',
    '(d8 && a2) -> X d8',
}

env_safe |= {
    """(d0 && !a0 && !a2) -> X ((d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8) || 
                       (!d1 && !d0 && !d6 && d3 && !d4 && !d5 && !d7 && !d8))""",
    """(d1 && !a1 && !a2) -> X ((!d1 && d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8) ||
                        (!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8))""",
    """(d3 && !a3 && !a2) -> X ((!d1 && d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8) ||
                        (!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8) ||
                        (!d1 && !d0 && d6 && !d3 && !d4 && !d5 && !d7 && !d8))""",
    """(d4 && !a4 && !a2) -> X ((!d1 && !d0 && !d6 && d3 && !d4 && !d5 && !d7 && !d8) || 
                        (d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)|| 
                        (!d1 && !d0 && !d6 && !d3 && !d4 && d5 && !d7 && !d8) || 
                        (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && d7 && !d8))""",
    """(d5 && !a5 && !a2) -> X ((!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8) || 
                        (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && d8))""",
    """(d6 && !a6 && !a2) -> X ((!d1 && !d0 && !d6 && d3 && !d4 && !d5 && !d7 && !d8) || 
                         (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && d7 && !d8))""",
    """(d7 && !a7 && !a2) -> X ((!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8) || 
                         (!d1 && !d0 && d6 && !d3 && !d4 && !d5 && !d7 && !d8) || 
                         (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && d8))""",
    """(d8 && !a8 && !a2) -> X ((!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && d7 && !d8) || 
                         (!d1 && !d0 && !d6 && !d3 && !d4 && d5 && !d7 && !d8))""",
    }
# (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)
# singularity requirement (didn't work)
# env_safe.add(synth.exactly_one(
#     {'d0', 'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8'}
# )[0])


# termination (defender wins):
env_safe |= {
    '(d0 && a0) -> X (!d1 && d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d1 && a1) -> X (d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d3 && a3) -> X (!d1 && !d0 && !d6 && d3 && !d4 && !d5 && !d7 && !d8)',
    '(d4 && a4) -> X (!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8)',
    '(d5 && a5) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && d5 && !d7 && !d8)',
    '(d6 && a6) -> X (!d1 && !d0 && d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d7 && a7) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && d7 && !d8)',
    '(d8 && a8) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && d8)',
}
# termination (attacker wins):
env_safe |= {
    '(d0 && a2) -> X (!d1 && d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d1 && a2) -> X (d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d3 && a2) -> X (!d1 && !d0 && !d6 && d3 && !d4 && !d5 && !d7 && !d8)',
    '(d4 && a2) -> X (!d1 && !d0 && !d6 && !d3 && d4 && !d5 && !d7 && !d8)',
    '(d5 && a2) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && d5 && !d7 && !d8)',
    '(d6 && a2) -> X (!d1 && !d0 && d6 && !d3 && !d4 && !d5 && !d7 && !d8)',
    '(d7 && a2) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && d7 && !d8)',
    '(d8 && a2) -> X (!d1 && !d0 && !d6 && !d3 && !d4 && !d5 && !d7 && d8)',
}


# objective
env_prog = {'True'}

# System variables and specification
sys_vars = {'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'}
sys_init = {'a0'}
sys_safe = {
    '(a0 && !d0) -> X (a1 || a3)',
    '(a1 && !d1) -> X (a0 || a4 || a2)',
    'a2 -> X a2',
    '(a3 && !d3) -> X (a0 || a4 || a6)',
    '(a4 && !d4) -> X (a1 || a3 || a5 || a7)',
    '(a5 && !d5) -> X (a4 || a2 || a8)',
    '(a6 && !d6) -> X (a3 || a7)',
    '(a7 && !d7) -> X (a4 || a6 || a8)',
    '(a8 && !d8) -> X (a7 || a5)',
}

# termination (defender wins):

sys_safe |= {
    '(d0 && a0) -> X a0',
    '(d1 && a1) -> X a1',
    '(d3 && a3) -> X a3',
    '(d4 && a4) -> X a4',
    '(d5 && a5) -> X a5',
    '(d6 && a6) -> X a6',
    '(d7 && a7) -> X a7',
    '(d8 && a8) -> X a8',
}

sys_safe.add(synth.exactly_one(
    {'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'}
)[0])

sys_prog = {'a2'}

# Create the specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)

# Controller synthesis
#
# At this point we can synthesize the controller using one of the available
# methods.
#
# @synthesize@
# Moore machines
# controller reads `env_vars, sys_vars`, but not next `env_vars` values
specs.moore = True
# Ask the synthesizer to find initial values for system variables
# that, for each initial values that environment variables can
# take and satisfy `env_init`, the initial state satisfies
# `env_init /\ sys_init`.
specs.qinit = '\E \A'  # i.e., "there exist sys_vars: forall sys_vars"

# At this point we can synthesize the controller
# using one of the available methods.


tic = time()
strategy = synth.synthesize(specs)
toc = time()

assert strategy is not None, 'unrealizable'
print(strategy)

print("processing time is ", toc-tic, "sec")

