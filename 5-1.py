import json
import re
import operator
from collections import Counter

p = None
with open('5-1.txt') as f:
    p = f.readline().strip()

#p = 'dabAcCaCBAcCcaDA'

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

print(p)
print(len(p))
