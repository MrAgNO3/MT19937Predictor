from functools import reduce
from tqdm import *


def getOne(l,var = 1,func = None):
    if func is not None:
        return [i for i,j in enumerate(l) if func(j)]
    return [i for i, j in enumerate(l) if j == var]

xor = lambda *arg:reduce(lambda a,b:a^b,arg)