from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os
import random
from math import ceil

random.seed('AgNO3')
Key = int.to_bytes(random.getrandbits(128),16)

def splitChunks(lst,chunk_size=16):
    return [lst[i:i+chunk_size] for i in range(0,len(lst),chunk_size)]

def kvParsing(s):
    pairs = [i.split('=') for i in s.split('&')]
    return {i:j for i,j in pairs}

def kvEncode(d):
    return '&'.join([f"{k}={v}" for k,v in d.items()])

def profile_for(email):
    if '&' in email or '=' in email:
        raise ValueError('Illegal char in email')
    p = {
        'email': email,
        'uid': 10,
        'role': 'user'
    }
    return kvEncode(p)

def encProfile(email):
    p = profile_for(email).encode()
    data = pad(p,16)
    # print("encrypt data:",splitChunks(data,16))
    aes = AES.new(key=Key,mode=AES.MODE_ECB)
    return aes.encrypt(data)

def decProfile(encData):
    aes = AES.new(key=Key,mode=AES.MODE_ECB)
    p = unpad(aes.decrypt(encData),16).decode()
    p = kvParsing(p)
    if p['role'] == 'admin':
        print('Yes, you are admin!')
    else:
        print('Sorry, only admin allowed.')


prefLen = len('email=')
prof1 = b'1'*(AES.block_size - prefLen)+pad(b'admin',16)
prof1 = prof1.decode()
paste = splitChunks(encProfile(prof1))[1]

prof2 = '1'*13  # Any email with a length of 13
enc2 = encProfile(prof2)
cut = splitChunks(enc2)
cut[-1] = paste

decProfile(b''.join(cut))
