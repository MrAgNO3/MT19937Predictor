from pwn import xor
from requests import get
from base64 import b64decode
from itertools import combinations
from chall3 import score

rkey = b'Terminator X: Bring the noise'
data = get('https://cryptopals.com/static/challenge-data/6.txt').content

def hammingDist(s1,s2):
    if isinstance(s1,str):
        s1 = s1.encode()
    if isinstance(s2,str):
        s2 = s2.encode()
    return int.from_bytes(xor(s1,s2)).bit_count()


t1 = 'this is a test'
t2 = 'wokka wokka!!!'
assert hammingDist(t1,t2) == 37

SampleCnt = 6
rec = {}
data = b64decode(data)

for keysize in range(2,40):
    blocks = [data[keysize*i:keysize*(i+1)] for i in range(SampleCnt)]

    dist = sum(hammingDist(s1,s2) for s1,s2 in combinations(blocks,2))
    normDist = dist/keysize/(SampleCnt*(SampleCnt-1)/2)
    rec[keysize] = normDist

rec = sorted([(ks,rec[ks]) for ks in rec],key=lambda x:x[1])
possibleKeysize = [i[0] for i in rec[:10]]
# possibleKeysize = [i[0] for i in rec[:1]]


for ks in possibleKeysize:
    key = []
    res = []
    blocks = [data[i-ks:i] for i in range(ks,len(data),ks)]
    blocks_ = [bytes(i) for i in zip(*blocks)]
    for i,b in enumerate(blocks_):
        # print(i)
        rec = {}
        for c in range(32,128):
            rec[c] = score(xor(b,c))
        rec = sorted([(c,rec[c]) for c in rec if rec[c]>0],key=lambda x:x[1],reverse=1)
        try:
            key.append(rec[0][0])
            res.append(xor(b,rec[0][0]))
        except:
            break

    print(f"keysize = {ks}")
    print(bytes(key))
    text = ''.join(bytes(t).decode() for t in zip(*res))
    print(text)
    print('\n\n' + '='*30 + '\n\n')
