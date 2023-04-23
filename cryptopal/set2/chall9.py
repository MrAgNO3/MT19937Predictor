from Crypto.Util.Padding import pad,unpad

s = b"YELLOW SUBMARINE"
ps = pad(s,20,"pkcs7")
# print(ps)
assert ps == b"YELLOW SUBMARINE\x04\x04\x04\x04"

ups = unpad(ps,20,'pkcs7')
# print(ups)
assert ups == s


def mypad(s,block_size,style='pkcs7'):
    f = lambda x:[x for _ in range(x)]
    if style == 'pkcs7':
        return s + bytes(f(block_size - len(s)%block_size))
    elif style == 'x923':
        raise NotImplementedError
    elif style == 'iso7816':
        raise NotImplementedError
    else:
        raise NotImplementedError


def myunpad(ps,block_size,style='pkcs7'):
    if style == 'pkcs7':
        return ps[:-ps[-1]]
    elif style == 'x923':
        raise NotImplementedError
    elif style == 'iso7816':
        raise NotImplementedError
    else:
        raise NotImplementedError

assert mypad(s,20) == ps
assert myunpad(ps,20) == s
