import random
import time
import copy
import sys
sys.path.append('./source')
from MT19937 import MT19937, MT19937_symbolic
from XorSolver import XorSolver


nbits = 16
print(f"{nbits = }")
rng = lambda: random.getrandbits(nbits)


rng_sym = MT19937_symbolic()
eqns = []
n_test = []

def readNdata():
    ndata = {}
    with open('record.txt') as f:
        for i in f.readlines():
            nb,nd = map(int,i.split(','))
            ndata[nb] = nd
    return ndata
try:
    ndata = readNdata()[nbits]
except:
    ndata = 624*int((31.9//nbits)+1)

for _ in range(ndata):
    
    # Get random number from rng and save for later testing
    n = rng()
    n_test.append(n)
    
    eqn_rhs_list = rng_sym._int2bits(n)
    eqn_lhs_list = rng_sym()[:nbits]
    
    # Add to eqns
    for lhs,rhs in zip(eqn_lhs_list, eqn_rhs_list):
        eqns.append([lhs,rhs])

### Using the python only solver XorSolver.solve

nvars = 624*32
nvars = nbits*624*int((31.9//nbits)+1)
eqns_copy = copy.deepcopy(eqns)

# Initialise solver with eqns
solver = XorSolver(eqns_copy, nvars)

t = time.time()

# Solve eqns. Takes aroung 100s to solve
# verbose=False to suppress output
solver.solve(verbose=True)

print("Time taken to solve: {}s".format(time.time() - t))

# Clone MT19937 with solver.eqns (fully solved by now)
rng_clone = MT19937(state_from_solved_eqns = solver.eqns)

# Test if cloning has been successful
for n in n_test:
    assert n == rng_clone(), "Clone failed!"
    
print("[*] Cloning successful!")