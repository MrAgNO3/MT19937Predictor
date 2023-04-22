import requests
from base64 import *


data = requests.get('https://cryptopals.com/static/challenge-data/8.txt')
# data = b64decode(data)
