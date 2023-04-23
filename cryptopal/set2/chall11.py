from chall10 import *
from random import getrandbits,randint
import re


def myECBenc(data,key=KEY):
    data = pad(data,AES.block_size)
    # data = [data[i:i+AES.block_size] for i in range(0,len(data)-1,AES.block_size)]
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return aes.encrypt(data)


def myECBdec(data,key=KEY):
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return unpad(aes.decrypt(data),16)


data = os.urandom(100)
a = AES.new(key=KEY,mode=AES.MODE_ECB)

assert myECBenc(data) == a.encrypt(pad(data,16))
assert myECBdec(myECBenc(data)) == data

def encryption_oracle(data):

    data = os.urandom(16)[:randint(5,10)] + data + os.urandom(16)[:randint(5,10)]
    data = pad(data,16)
    key = os.urandom(16)
    
    if getrandbits(1):
        encType = AES.MODE_CBC
        iv = os.urandom(16)
        aes = AES.new(key=key,iv=iv,mode=encType)
    else:
        encType = AES.MODE_ECB
        aes = AES.new(key=key,mode=encType)

    return aes.encrypt(data).hex(),encType


def checkEncType():
    data = b'0' * 100
    enc,t = encryption_oracle(data)
    enc = re.findall('[a-f0-9]{32}',enc)
    if len(enc) != len(set(enc)):
        assert t == AES.MODE_ECB
    else:
        assert t == AES.MODE_CBC

        
for _ in range(100):
    checkEncType()
    # print('Good')
