import random
import re
N = 624

def _int32(x):
    return int(0xFFFFFFFF & x)


class myRandom(random.Random):
    
    def seed(self,s):
        if s is None:
            super().seed(s)
            # print('super().seed')
            return
        if not isinstance(s,(int,bytes)):
            print(s,type(s))
            raise NotImplementedError

        if isinstance(s,int):
            if s == 0:
                key = [0]
            else:
                key = s.to_bytes((s.bit_length()-1)//8+1,'little').hex()
                # key = [s&0xffffffff,s>>32]
                key = [int.from_bytes(bytes.fromhex(i),'little') for i in re.findall('[a-f0-9]{1,8}',key)]
            return self.init_by_array(key)
        elif isinstance(s,bytes):
            raise NotImplementedError

    def init_genrand(self,sd):
        mt = [0] * 624
        mt[0] = sd
        mti = 1
        while mti < N:
            mt[mti] = _int32((1812433253 * (mt[mti-1] ^ (mt[mti-1] >> 30))) + mti)
            mti += 1
        # self.index = mti
        return mt

    def init_by_array(self, init_key):
        mt = self.init_genrand(19650218)
        i, j = 1, 0
        key_length = len(init_key)
        # print(f"{key_length = }")
        # print([hex(i) for i in init_key])
        k = N if N > key_length else key_length
        while k:
            mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1664525)) + init_key[j] + j
            mt[i] = _int32(mt[i])
            i += 1
            j += 1
            if i >= N:
                mt[0] = mt[N-1]
                i = 1
            if j >= key_length:
                j = 0
            k -= 1
        k = N - 1
        while k:
            mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 30)) * 1566083941)) - i
            mt[i] = _int32(mt[i])
            i += 1
            if i >= N:
                mt[0] = mt[N-1]
                i = 1
            k -= 1
        mt[0] = 0x80000000
        return mt
        state = (3,tuple(mt + [0]),False)
        super().setstate(state)

import os
for _ in range(100):
    s = int.from_bytes(os.urandom(100))
    # s = os.urandom(100)
    # s = 0x1122334455667788
    r = myRandom()
    s0 = r.seed(s)
    rr = random.Random()
    rr.seed(s)
    s1 = list(rr.getstate()[1][:-1])
    print(s0 == s1)
    # input()
