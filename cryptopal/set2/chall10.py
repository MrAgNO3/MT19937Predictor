from requests import get
from base64 import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from pwn import xor
import os


data = get('https://www.cryptopals.com/static/challenge-data/10.txt').content.split(b'\n')
data = [b64decode(i) for i in data]
KEY = b"YELLOW_SUBMARINE"

def singleEnc(data,key=KEY):
    data = pad(data,AES.block_size)[:AES.block_size]
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return aes.encrypt(data)

def singleDec(data,key=KEY):
    # data = pad(data,AES.block_size)[:AES.block_size]
    aes = AES.new(key=key,mode=AES.MODE_ECB)
    return aes.decrypt(data)

def myCBCenc(data,iv=bytes(AES.block_size),key=KEY):
    data = pad(data,AES.block_size)
    data = [data[i:i+AES.block_size] for i in range(0,len(data)-1,AES.block_size)]
    res = [singleEnc(xor(data[0],iv),key=key)]
    # data[0] = xor(data[0],iv)
    for i in data[1:]:
        res.append(singleEnc(xor(i,res[-1]),key=key))
    return b''.join(res)


def myCBCdec(data,iv=bytes(AES.block_size),key=KEY):
    data = [data[i:i+AES.block_size] for i in range(0,len(data)-1,AES.block_size)]
    res = [xor(singleDec(i,key=key),j) for i,j in zip(data,[iv]+data)]
    return unpad(b''.join(res),AES.block_size)



res = myCBCenc(data[0])
a = AES.new(key=KEY,mode=AES.MODE_CBC,iv=bytes(16))

assert myCBCenc(data[0]) == a.encrypt(pad(data[0],16))
assert myCBCdec(myCBCenc(data[0])) == data[0]
