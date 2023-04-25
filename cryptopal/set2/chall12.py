from requests import get
from base64 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os
import random
from math import ceil


unknown_str = b64decode('''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK''')
random.seed('AgNO3')
# unknown_str = b'AgNO3AgNO3AgNO3'
Key = int.to_bytes(random.getrandbits(128),16)


def ECBenc(data):
    data = pad(data,16)[:16]
    aes = AES.new(key=Key,mode=AES.MODE_ECB)
    return aes.encrypt(data)

def encryption_oracle(data,key=Key):
    data = pad(data + unknown_str,16)
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return aes.encrypt(data)

# Detect the length of the unkown string
res = encryption_oracle(b'')
for pl in range(17):
    padLength = pl
    if len(encryption_oracle(b'1'*pl)) != len(res):
        break
    
L = len(res) - padLength
prefix = b'\x00' * (padLength%16)

# Detect the encrypt type
enc = encryption_oracle(b'A'*100)
enc = [enc[i:i+16] for i in range(0,len(enc),16)]
assert len(enc) > len(set(enc)),"Not a ECB encryption"


def testChar(encData,known_str):
    # print(encData,known_str)
    for c in range(0x100):
        data = bytes([c]) + known_str
        if ECBenc(data) == encData:
            return bytes([c])
        
s = b''

for b in range(ceil(len(res)/AES.block_size)):
    for c in range(1,16):
        enc = encryption_oracle(b'\x00'*(16*b+c) + prefix)
        enc = [enc[i:i+16] for i in range(0,len(enc),16)]
        s = testChar(enc[-b-1],s) + s
    enc = encryption_oracle(b'\x00'*(16*b+16) + prefix)
    enc = [enc[i:i+16] for i in range(0,len(enc),16)]
    s = testChar(enc[-b-2],s) + s

s = s[len(prefix):]
print(s.decode())
assert s == unknown_str
