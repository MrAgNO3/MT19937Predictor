## Set 1 Chall 4
import requests
from chall3 import score
from tqdm import tqdm
from pwn import xor


data = requests.get('https://cryptopals.com/static/challenge-data/4.txt')
data = data.text.split('\n')

rec = []
b = bytes.fromhex

for i,h in enumerate(data):
    # print(f"{i}/{len(data)}",end='\r')
    print(i)
    s = [xor(b(h),c) for c in range(128)]
    scores = [(i,j,score(j)) for i,j in enumerate(s)]
    scores = [i for i in scores if i[2] > 0]
    rec.extend(scores)

for i in rec:
    print(*i)

# 53 b'Now that the party is jumping\n' 0.4856266666666667
