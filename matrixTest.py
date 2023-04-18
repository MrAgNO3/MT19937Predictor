import IPython
import gzip, sys, time, copy, random
sys.path.append('./source')
from MT19937 import MT19937, MT19937_symbolic
from XorSolver import XorSolver
from Gauss import Gauss
import numpy as np
from AgNO3 import *
from functools import reduce
from tqdm import *
from math import ceil

nbits = 24
V = 1
if len(sys.argv) == 2:
    nbits = int(sys.argv[-1])
print(f"{nbits = }")

# input('> ')


rng_sym = MT19937_symbolic()
eqns = []
n_test = []
itrr = 624*int((31.9//nbits)+1)
itrr = ceil(19968/nbits)
for _ in range(itrr):
    if V:print(f"Build equations:{_}/{itrr}",end='\r')
    lhs = rng_sym()
    eqns.extend(lhs[:nbits])

def readMat(nb):
    iterr = int(31.9//nb + 1)
    ndata = 624*iterr
    inv_filename = "matrices/inverse_nb-{}_iterr-{}_ndata-{}.npy.gz".format(nb, iterr, ndata)
    ver_filename = "matrices/verify_nb-{}_iterr-{}_ndata-{}.npy.gz".format(nb, iterr, ndata)
    f = gzip.GzipFile(inv_filename, "r")
    solve_mat = np.load(f, allow_pickle=True)
    f = gzip.GzipFile(ver_filename, "r")
    verify_mat = np.load(f, allow_pickle=True)
    f.close()
    return solve_mat,verify_mat

def toByteArray(l):
    n = np.zeros(19968,dtype=np.bool_)
    for i in l:
        n[i] ^= True
    return n

print("Building ee")
ee = np.array([toByteArray(i) for i in eqns],dtype=np.bool_)



tst = rng_sym.twist_mat
tstm = np.mat([toByteArray(i) for i in tst])

try:
    r1,r2 = readMat(nbits)
    err = []
    for i in list(range(32)) + [100,200,300,400,114,1145,11451,19967,15000,11233,3213,9999,8888,4567]:
        try:
            assert xor(*[eqns[i] for i in r1[i]]) == set([i])
        except:
            err.append(i)
    print(f"{len(err) = },{err = }")
except:
    print("Check Julias'mat failed.")
# for i in range(1,32):
#     ee[i, i] ^= 1
#     ee[i*(i+101), i] ^= 1
ext_ee = np.concatenate((ee,np.eye(ee.shape[0],dtype=np.bool_)),axis=1)
fix = np.zeros((31,ext_ee.shape[1]),dtype=bool)
for i in range(31):
    fix[i,i+1] ^= 1
ext_ee = np.concatenate((ext_ee,fix))
res,novar = Gauss(ext_ee,v=1)
myMat = res[:19968,19968:]
print(sum([res[i,i] for i in range(19968)]) )
assert sum([res[i,i] for i in range(19968)]) == 19968

print("Transforming matrix.")
myMat_ = np.array([set(getOne(i)) for i in tqdm(myMat)])
with gzip.GzipFile(f"myMat{nbits}.npy.gz",'w') as f:
    np.save(f,myMat_,allow_pickle=True)
    print(f"Saved as myMat{nbits}.npy.gz")
