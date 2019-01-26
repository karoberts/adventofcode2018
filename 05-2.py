import json
import re
import operator
from collections import Counter

def react(p):
    i = 0
    remove = 0
    while True:
        i = max(0, remove - 1)
        remove = -1
        while i < len(p) - 1:
            c1 = p[i]
            c2 = p[i + 1]
            c1l = c1.islower()
            c2l = c2.islower()
            c1u = c1.upper()
            c2u = c2.upper()
            if c1u == c2u and (c1l != c2l):
                remove = i
                break
            i += 1

        if remove == -1:
            break;
        
        #print(len(p))
        #print('before', p, 'r', remove)
        #print('r', remove)
        p = p[0:remove] + p[remove+2:]
        #print('after', p)

    return p

p = None
with open('05.txt') as f:
    p = f.readline().strip()

#p = 'dabAcCaCBAcCcaDA'

lens = []
lets = []
for ch_ in range(ord('a'), ord('z')):
    ch = chr(ch_)
    p_ = p.translate({ ord(ch.lower()): None,  ord(ch.upper()): None})
    p_ = react(p_)
    lens.append((len(p_), ch))

print(min(lens, key=lambda x:x[0]))
