## Set 1 Chall 3
from pwn import xor
import string
import re
from collections import Counter

def score(btext):
    try:
        text = btext.decode(errors='ignore')
    except:
        return 0
    
    # 英文中单词以空格分隔，有时候不便用空格就用'_'代替(如flag)
    if ' ' not in text and '_' not in text:
        return 0
    
    # 计算可打印字符的比例
    printable_chars = [char for char in text if char in string.printable]
    printable_ratio = len(printable_chars) / len(text)
    if printable_ratio < 1:
        return 0

    # 英文字母的比例
    letter_chars = [c for c in text if c in string.ascii_letters]
    letter_freq = len(letter_chars)/len(text)
    if letter_freq < 0.5:
        return 0

    # 不正常的标点符号的比例，去掉了句子结尾的符号、单引号和连字符号
    strange_punctuation = '"#$%&()*+/:<=>@[\\]^`{|}~'
    sp_chars = [i for i in text if i in strange_punctuation]
    sp_ratio = len(sp_chars)/len(text)
    if sp_ratio > 0.05:
        return 0

    punctuation = '\',.-?!'
    p_chars = [i for i in text if i in punctuation]
    p_ratio = len(p_chars)/len(text)
    if p_ratio > 0.1:
        return 0
    
    # 计算字母出现的频率
    letter_counter = Counter([char.lower() for char in text if char.isalpha()])
    letter_freqs = {char: count / sum(letter_counter.values()) for char, count in letter_counter.items()}
    english_letter_freqs = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228,
                            'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
                            'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987,
                            's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
                            'y': 0.01974, 'z': 0.00074}
    letter_similarity = sum([abs(freq - english_letter_freqs.get(char, 0)) for char, freq in letter_freqs.items()])
    
    # 计算单词平均长度
    # 对于非连续的文本，这一项不需要，比如s1c6
    words = re.findall(r'\w+', text)
    words = text.split(' ')
    avg_word_len = sum(len(word) for word in words) / len(words)
    english_avg_word_len = 4.7
    word_len_similarity = abs(avg_word_len - english_avg_word_len) / english_avg_word_len
    if avg_word_len > 10 or avg_word_len < 4:
        pass
        # return 0

    # 去掉不正常的字符串后，以字母频率为基准
    return letter_similarity


b = bytes.fromhex
h = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
s = [xor(b(h),c) for c in range(128)]
scores = [(i,j,score(j)) for i,j in enumerate(s)]
scores = [i for i in scores if i[2] > 0]
scores.sort(key=lambda x:x[2],reverse=1)


# 88 b"Cooking MC's like a pound of bacon"
