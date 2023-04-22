## Set 1 Chall 2

from pwn import xor
h1 = '1c0111001f010100061a024b53535009181c'
h2 = '686974207468652062756c6c277320657965'
b = bytes.fromhex
# print(xor(b(h1),b(h2)).hex())
