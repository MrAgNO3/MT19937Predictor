import requests
from base64 import *
import re

data = requests.get('https://cryptopals.com/static/challenge-data/8.txt').text
data = data.split('\n')

for d in data:
    dd = re.findall('[0-9a-f]{32}',d)
    if len(dd) != len(set(dd)):
        print(dd)
