import json
import re
import operator
from collections import Counter

dupemap = {}

def manhat_dist(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def manhat_distxy(c, x, y):
    return abs(c[0] - x) + abs(c[1] - y)

def manhat_diststr(c, xystr):
    #print(xystr)
    m = pat.match(xystr)
    return manhat_distxy(c, int(m.group(1)), int(m.group(2)))

def find(cs, c, maxdist, distmap):
    visited = set()
    _find(cs, c, maxdist, c[0] + 1, c[1], visited, distmap)
    _find(cs, c, maxdist, c[0], c[1] + 1, visited, distmap)
    _find(cs, c, maxdist, c[0] - 1, c[1], visited, distmap)
    _find(cs, c, maxdist, c[0], c[1] - 1, visited, distmap)
    pass

def _find(cs, c, maxdist, x, y, visited, distmap):
    key = str(x) + ',' + str(y)
    if key in visited:
        return
    visited.add(key)

    dist = manhat_distxy(c, x, y)
    if key in distmap:
        #if key == '3,8':
            #print('refind', dist, c, distmap[key], dupemap[key])
        if distmap[key][0] == 0:
            return
        if distmap[key][1] is not None and distmap[key][1][2] == c[2]:
            return
        if distmap[key][0] == -1 or distmap[key][0] == dist:
            distmap[key] = (-1, None)
        if distmap[key][0] > dist:
            distmap[key] = (dist, c)
    else:
        #if key == '3,8':
            #print('first', dist, c)
        distmap[key] = (dist, c)

    if key not in dupemap:
        dupemap[key] = set()
    dupemap[key].add(c)

    if dist > maxdist:
        #distmap[key] = (-2, c)
        return

    _find(cs, c, maxdist, x + 1, y, visited, distmap)
    _find(cs, c, maxdist, x, y + 1, visited, distmap)
    _find(cs, c, maxdist, x - 1, y, visited, distmap)
    _find(cs, c, maxdist, x, y - 1, visited, distmap)
    pass

pat = re.compile(r'^([\-\d]+),[ ]?([\-\d]+)$')
coords = []
with open('06-1.txt') as f:
    ch = 'A'
    for line in f:
        m = pat.match(line.strip())
        coords.append((int(m.group(1)), int(m.group(2)), ch))
        ch = chr(ord(ch) + 1)

print('coords', coords)
#print(manhat_dist(coords[3], coords[4]))

maxdist_map = {}
maxdist_map2 = {}
ch = 'A'
for i in range(0, len(coords)):
    maxd = 0
    for j in range(0, len(coords)):
        if i == j:
            continue
        dist = manhat_dist(coords[i], coords[j])
        if dist > maxd:
            maxd = dist
    maxdist_map[i] = maxd
    maxdist_map2[ch] = maxd
    ch = chr(ord(ch) + 1)

print('maxdist', maxdist_map)

distmap = {}
for i in range(0, len(coords)):
    distmap[str(coords[i][0]) + ',' + str(coords[i][1])] = (0, coords[i])
for i in range(0, len(coords)):
    find(coords, coords[i], maxdist_map[i], distmap)
for k, v in dupemap.items():
    if len(v) == 1:
        continue
    mind = 99999999
    minc = None
    for c in v:
        d = manhat_diststr(c, k)
        #if k == '3,8':
        #    print('match', d, c, mind, minc)
        if d < mind:
            mind = d
            minc = c
        elif d == mind:
            mind = -1
            minc = None
            break
#    if k == '3,8':
#        print('dupe', k, 'assign', minc, mind)
    distmap[k] = (mind, minc)

#print('dupe', dupemap)
#print('dist', distmap)

totmap = {}
infmap = {}
for k, v in distmap.items():
    d = v[0]
    if v[1] is None:
        continue
    c = v[1][2]
    if d > 0:
        if c not in totmap:
            totmap[c] = 1
        else:
            totmap[c] += 1
    if d > maxdist_map2[c]:
        infmap[c] = True

#print('infs', infmap)
#print('tots', totmap)

finalmap = {}
for k2, v2 in distmap.items():
    d = v2[0]
    if v2[1] is None:
        continue
    c = v2[1][2]
    if c in infmap:
        continue

    if c not in finalmap:
        finalmap[c] = 0
    finalmap[c] += 1
    print('p', c, k2)

print('final', finalmap)
