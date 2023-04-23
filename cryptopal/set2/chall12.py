from requests import get
from base64 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os
import random

unknown_str = b64decode('''Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK''')
random.seed('AgNO3')
Key = int.to_bytes(random.getrandbits(128),16)


def encryption_oracle(data,key=Key):
    data = pad(data + unknown_str,16)
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return aes.encrypt(data)


# Detect the length of the unkown string
res = encryption_oracle(b'')
for pl in range(16):
    padLength = pl
    if len(encryption_oracle(b'1'*pl)) != len(res):
        break

L = len(res) - padLength

S = ''
