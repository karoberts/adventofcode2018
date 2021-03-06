import json
import re
import operator
from collections import Counter

pat = re.compile(r'^$')

def readit(pos):
    nchild = es[pos]
    nmeta = es[pos + 1]
    amt = 2
    for i in range(0, nchild):
        amt += readit(pos + amt)
    for i in range(0, nmeta):
        meta.append(es[pos + amt + i])
    
    return amt

with open('08.txt') as f:
    for line in f:
        es = [int(x) for x in line.strip().split(' ')]

s = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
#es = [int(x) for x in s.split(' ')]

meta = []
nodevals = {}
nodekids = {}
#print(es)

i = 0
stack = []
while i < len(es):

    nptr = i
    nchild = es[i]
    nmeta = es[i + 1]
    nodevals[nptr] = 0
    nodekids[nptr] = []

    #print('i', i, nchild, nmeta, stack)

    if nchild > 0:
        stack.append((i, 0))
        i += 2
        nodekids[nptr].append(i)
        continue

    i += 2
    for j in range(0, nmeta):
        nodevals[nptr] += (es[j + i])
    i += nmeta

    while len(stack) > 0:
        parent = stack.pop()
        curchild = parent[1] + 1
        nchildren = es[parent[0]]
        if curchild == nchildren:
            val = 0
            for j in range(0, es[parent[0] + 1]):
                kidi = es[j + i] - 1
                if kidi >= len(nodekids[parent[0]]):
                    continue
                val += nodevals[nodekids[parent[0]][kidi]]
            nodevals[parent[0]] = val
            i += es[parent[0] + 1]
            continue
        nodekids[parent[0]].append(i)
        stack.append((parent[0], curchild))
        break
            
#print(i, len(es))
#print(stack)
#print(meta)
#print(nodekids)
#print(nodevals)
print(nodevals[0])
