import numpy as np
from AgNO3 import *
from f61d import timeit


def Gauss(x,v = 0,*args,**kwargs):
    m,n = x.shape
    # print(f"Gaussing, Shape:{m = },{n = }\n\n\n")
    # m个方程 n-1个变量
    # assert m >= n-1 # (不一定)
    res = x.copy()
    novar = []
    
    if v:
        from tqdm import tqdm
        bar = tqdm(range(min(n,m)),*args,**kwargs)
    else:
        bar = range(min(n,m))
        
    for i in bar:
        op = i
        try:
            while not res[op,i]:
                op += 1
        except:
            novar.append(i)
            op = i
            # res[i,i] ^= True
            continue
        
        if op != i:
            res[[op,i],:] = res[[i,op],:]

        # 化为RREF
        for j in range(0,m):
            if not res[j,i]:
                continue
            if j == i:
                continue
            res[j] ^= res[i]

    # 化为RREF
    # for i in tqdm(range(m)):
    #     for j in range(i+1,min(m,n)):
    #         if res[i,j]:
    #             res[i] ^= res[j]

    return res,novar


@timeit
def XorGauss(x):
    m,n = x.shape
    res = x.copy()
    print(f"XorGaussing, Shape:{m = },{n = }")
    # m个方程 n-1个变量
    used = set()
    novar = []
    for var in range(min(m,n)):
        col = set(getOne(res[:,var]))
        try:
            cc = col ^ col & used
            slct = cc.pop()
        except:
            novar.append(var)
            continue
        used.add(slct)
        for i in col:
            if i == slct:
                continue
            res[i] ^= res[slct]
    return res,novar

if __name__ == '__main__':
    N = 15
    dt = np.bool_

    ans = np.random.randint(0,2,N).astype(dt)
    A = np.random.randint(0,2,(N,N)).astype(dt)
    b = np.array([sum(i*ans)%2 for i in A]).astype(dt)
    Ab = np.concatenate((A,b.reshape(N,1)),1)

    print(f"ans : \n{ans.astype(int)}")
    r_mat, novar = Gauss(Ab)
    # r_mat2,novar2 = XorGauss(Ab)

    r = r_mat[:,-1]
    print(f"res : \n{r_mat.astype(int)}")
    wrong = [i for i in range(N) if ans[i] != r[i]]
    print(wrong,novar)
    if all(i in novar for i in wrong):
        print("Success")
    else:
        print("Failed")