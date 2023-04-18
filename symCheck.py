import IPython
import gzip, sys, time, copy, random
sys.path.append('./source')
from MT19937 import MT19937, MT19937_symbolic
from XorSolver import XorSolver
from Gauss import Gauss
from tqdm import *
import numpy as np
from AgNO3 import *
from functools import reduce

nbits = 32
V = 0
if len(sys.argv) == 2:
    nbits = int(sys.argv[-1])
print(f"{nbits = }")

rng_sym = MT19937_symbolic()

random.seed(b'AgNO3')
state = random.getstate()[1][:-1]
state_flat = reduce(lambda a,b:a+b,[rng_sym._int2bits(i,bits=32) for i in state])

for block in range(10):
    sym = rng_sym()
    rd = bin(random.getrandbits(nbits))[2:].zfill(nbits)
    for b in range(nbits):
        assert reduce(lambda a,b:a^b,[state_flat[i] for i in sym[b]]) == bool(int(rd[b]))

def toByteArray(l):
    n = np.zeros(19968,dtype=np.bool_)
    for i in l:
        n[i] ^= True
    return n

r = rng_sym.twist_mat
r_mat = np.mat([toByteArray(i) for i in r])