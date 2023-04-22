from pwn import xor

m1 = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

key = b"ICE"

print(xor(key,m1).hex())
