import gzip, sys, time, copy, random
sys.path.append('./source')
from MT19937 import MT19937, MT19937_symbolic
from Gauss import Gauss
import numpy as np
from AgNO3 import *
from tqdm import *
from math import ceil

NBITS = [1,2,3,4,5,6,8,10,12,14,16,18,20,22,24,26,28,30,32][::-1]
NBITS = [5]
V = 1
def toByteArray(l):
    n = np.zeros(19968,dtype=np.bool_)
    for i in l:
        n[i] ^= True
    return n


def solveMat(it,*args,**kwargs):
    rng_sym = MT19937_symbolic()
    eqns = []
    n_test = []

    for _ in range(it):
        # if V: print(f"Build equations:{_}/{it}", end='\r')
        lhs = rng_sym()
        eqns.extend(lhs[:nbit])

    ee = np.array([toByteArray(i) for i in eqns], dtype=np.bool_)
    ext_ee = np.concatenate((ee, np.eye(ee.shape[0], dtype=np.bool_)), axis=1)
    fix = np.zeros((31, ext_ee.shape[1]), dtype=bool)
    for i in range(31):
        fix[i, i + 1] ^= 1
    ext_ee = np.concatenate((ext_ee, fix))
    res, novar = Gauss(ext_ee, v=1, colour='green',*args,**kwargs)
    return res

def genMat(nbit):
    max_itrr = int((31.9//nbit)+1) * 624
    min_itrr = ceil(19968/nbit)
    max_itrr = 4992
    min_itrr = 4368
    while not min_itrr >= max_itrr:
        itrr = (min_itrr + max_itrr) // 2
        res = solveMat(itrr, desc=f"{min_itrr}/{itrr}/{max_itrr} Gauss ")
        if not sum([res[i, i] for i in range(19968)]) == 19968:
            print("\nFailed")
            min_itrr = itrr + 1
            continue
        print("\nSuccess")
        max_itrr = itrr - 1

    itrr = (min_itrr + max_itrr) // 2
    res = solveMat(itrr, desc=f"{min_itrr}/{itrr}/{max_itrr} FinalGauss ")
    myMat = res[:19968, 19968:]
    myMat_ = np.array([set(getOne(i)) for i in tqdm(myMat,desc=f"{min_itrr}/{itrr}/{max_itrr} Transform ", colour='blue')])
    with gzip.GzipFile(f"myMat{nbit}.npy.gz", 'w') as f:
        np.save(f, myMat_, allow_pickle=True)
        print(f"Saved as myMat{nbit}.npy.gz")
    with open('record.txt','a') as rec:
        rec.write(f'{nbit},{itrr}\n')

bar = tqdm(NBITS,position=0,colour='red')
for nbit in bar:
    bar.set_description(f'nbit:{nbit} ')
    genMat(nbit)




def tamper(self):
    if self.mti == 0:
        self.twist()
    y = self.mt[self.mti]
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    self.mti = (self.mti + 1) % 624
    return _int32(y)