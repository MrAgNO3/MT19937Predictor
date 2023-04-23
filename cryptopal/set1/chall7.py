from requests import get
from base64 import *
from Crypto.Cipher import AES

key = b'YELLOW SUBMARINE'
data = get('https://cryptopals.com/static/challenge-data/7.txt').content
aes = AES.new(key=key,mode=AES.MODE_ECB)

data = b64decode(data)
t = aes.decrypt(data)
print(t.decode())
