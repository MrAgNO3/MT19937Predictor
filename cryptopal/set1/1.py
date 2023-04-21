## Set 1 Chall 1

from base64 import b64encode
h1 = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

# print(b64encode(bytes.fromhex(h1)))


## Set 1 Chall 2

from pwn import xor
h1 = '1c0111001f010100061a024b53535009181c'
h2 = '686974207468652062756c6c277320657965'
b = bytes.fromhex
# print(xor(b(h1),b(h2)).hex())


## Set 1 Chall 3
h = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
for c in range(128):
    # print(c,xor(b(h),c))
    pass

# 88 b"Cooking MC's like a pound of bacon"

## Set 1 Chall 4
import requests
data = requests.get('https://cryptopals.com/static/challenge-data/4.txt')
data = data.text
