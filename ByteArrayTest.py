import random
import time
import copy
# Quick hack
import sys
import IPython
# sys.path.append('./source')
from source.MT19937 import MT19937, MT19937_symbolic
from source.XorSolver import XorSolver
import numpy as np
from Gauss import Gauss
from AgNO3 import *
import os

random.seed(os.urandom(64))
stt0 = random.getstate()[1][:-1]
nbits = 32
V = 1

if len(sys.argv) == 2:
    nbits = int(sys.argv[-1])
print(f"{nbits = }")
rng = lambda: random.getrandbits(nbits)

# Init MT199937 symbolic
rng_sym = MT19937_symbolic()

# Build system of equations
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
    print("ReadNdataSuccess")
except:
    ndata = 624*int((31.9//nbits)+1)
    print("ReadNdataFailed")

pref = []
for _ in range(100):
    pref.append(rng())

for _ in range(ndata):
    if V:print(f"Build equations:{_}/{ndata}\r",end='')
    # Get random number from rng and save for later testing
    n = rng()
    n_test.append(n)
    
    eqn_rhs_list = rng_sym._int2bits(n,bits = nbits)
    eqn_lhs_list = rng_sym()
    
    for lhs,rhs in zip(eqn_lhs_list, eqn_rhs_list):
        eqns.append([lhs,rhs])

def toByteArray(l):
    n = np.zeros(19969,dtype=np.bool_)
    for i in l[0]:
        n[i] ^= True
    n[-1] = l[1]
    return n

# eqns_A = np.array([toByteArray(i[0]) for i in eqns],dtype=np.bool_)
# eqns_b = np.array([np.array(i[1]) for i in eqns],dtype=np.bool_)
t1 = time.time()
ee = np.array([toByteArray(i) for i in eqns],dtype=bool)
fix = np.zeros((31,ee.shape[1]),dtype=bool)
for i in range(31):
    fix[i,i+1] ^= 1
ee = np.concatenate((ee,fix))
r_mat,novar = Gauss(ee,v=V)
r = r_mat[:,-1]
if len(r)> 19968:
    r = r[:19968]
r = [[{i},j] for i,j in enumerate(r)]

print("Gauss end, %.2fs"%(time.time() - t1))

# nvars = nbits*624*int((31.9//nbits)+1)
nvars = nbits * ndata
eqns_copy = copy.deepcopy(eqns)

solver = XorSolver(eqns_copy, nvars)
t = time.time()
solver.solve(verbose=V)
se = sorted(solver.eqns,key=lambda x:x[0])
print("Time taken to solve: %.2fs"%(time.time() - t))
# solverRes = np.zeros(19968,dtype=np.bool_)
solverRes = [False]*19968
for i in solver.eqns:
    for j in i[0]:
        solverRes[j] = i[1]

wrong_ind = [i for i in range(19968) if r[i][1] != solverRes[i]]
if len(wrong_ind) == 0:
    print('All right')



rng_clone1 = MT19937(state_from_solved_eqns = solver.eqns)
rng_clone1()
RD1 = random.Random()
RD1.setstate((3,tuple(rng_clone1.state+[0]),None))
stt1 = RD1.getstate()[1][:-1]
res1 = []
for n in n_test:
    # assert n == rng_clone(), "Clone failed!"
    res1.append(int(n == RD1.getrandbits(nbits)))

rng_clone2 = MT19937(state_from_solved_eqns = r)
rng_clone2()
RD2 = random.Random()
RD2.setstate((3,tuple(rng_clone2.state+[0]),None))
stt2 = RD2.getstate()[1][:-1]
res2 = []
for n in n_test:
    # assert n == rng_clone(), "Clone failed!"
    res2.append(int(n == RD2.getrandbits(nbits)))

check = lambda x:print(f"{sum(x)}/{len(x)} RIGHT")
check(res1)
check(res2)

state0 = random.getstate()[1][:-1]
state1 = RD1.getstate()[1][:-1]
state2 = RD2.getstate()[1][:-1]

assert state1 == state2
t = [i for i,j in enumerate(state1) if j in state0]
breakpoint()
# >>> len(t)
# Out[16]: 102(522-623) / 203(421-623) / 100(524,623)

for _ in range(624):
    assert random.getrandbits(32) == RD1.getrandbits(32)
# Twist

state0_ = random.getstate()[1][:-1]
state1_ = RD1.getstate()[1][:-1]

t1 = [i for i,j in enumerate(state1_) if j in state0_]
assert state1[524:] == state0[:100]
assert state1_[:523] == state0[100:]
assert state1_[524:] == state0_[:100]
# >>> len(t1)
# Out[40]: 522
# >>> t1[0]
# Out[41]: 0
# >>> t1[-1]
# Out[42]: 521


for _ in range(10000):
    assert random.getrandbits(32) == RD1.getrandbits(32)

