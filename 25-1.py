import re
import sys
import json
from collections import defaultdict

sets = []
with open('25.txt') as f:
    for line in (l.strip() for l in f):
        coords = [int(x) for x in line.split(',')]
        coords.append(line)
        s = { line: coords }
        sets.append(s)

dist_memo = {}

def manhat_dist(id1, p1, id2, p2):
    k = id1 + id2
    if k in dist_memo: return dist_memo[k]
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])

def process():
    ret = []
    for i in range(0, len(sets)):
        s1 = sets[i]
        for id1, coord1 in s1.items():
            for j in range(i + 1, len(sets)):
                s2 = sets[j]
                if id1 in s2: continue

                for id2, coord2 in s2.items():
                    if manhat_dist(id1, coord1, id2, coord2) <= 3:
                        ret.append((s1, s2))
    return ret

c = -1
while True:
    rets = process();
    for ss in rets:
        for k, v in ss[1].items():
            ss[0][k] = v
        ss[1].clear()
    sets = [s for s in sets if len(s) > 0]
    if len(sets) == c:
        break
    c = len(sets)
    print(len(sets))

# < 1272

print('part1', len(sets))