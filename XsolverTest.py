import random
import time
import copy
# Quick hack
import sys
import IPython

sys.path.append('./source')

# Import symbolic execution
from MT19937 import MT19937, MT19937_symbolic

# Import XorSolver
from XorSolver import XorSolver


### Creating the equations to solve

# Init python's getrandbits with 32 bits
nbits = 32
if len(sys.argv) == 2:
    nbits = int(sys.argv[-1])
print(f"{nbits = }")
rng = lambda: random.getrandbits(nbits)

# Init MT199937 symbolic
rng_sym = MT19937_symbolic()

# Build system of equations
eqns = []
n_test = []
# for _ in range(624):
for _ in range(624*int((31.9//nbits)+1)):
    print(f"Build equations:{_}/{624*int((31.9//nbits)+1)}\r",end='')
    # Get random number from rng and save for later testing
    n = rng()
    n_test.append(n)
    
    # Split n into binary (A list of bools)
    eqn_rhs_list = rng_sym._int2bits(n,bits = nbits)
    
    # Get symbolic representation of n
    eqn_lhs_list = rng_sym()
    
    # Add to eqns
    for lhs,rhs in zip(eqn_lhs_list, eqn_rhs_list):
        eqns.append([lhs,rhs])

print()
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

# input('Solve over')
IPython.embed()

# Clone MT19937 with solver.eqns (fully solved by now)
rng_clone = MT19937(state_from_solved_eqns = solver.eqns)
rng_clone()
RD = random.Random()
RD.setstate((3,tuple(rng_clone.state+[0]),None))

# Test if cloning has been successful
res = [0,0]
for n in n_test:
    # assert n == rng_clone(), "Clone failed!"
    res[int(n == RD.getrandbits(nbits))] += 1
    
if res[0] == 0:
    print("[*] Cloning successful!")
else:
    print(f"Failed!!!\nsuc:{res[1]}\nfail:{res[0]}")
# IPython.embed()
