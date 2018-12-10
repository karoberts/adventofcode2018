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

pat = re.compile(r'^([\-\d]+),[ ]?([\-\d]+)$')
coords = []
minx = 999999999
maxx = 0
miny = 999999999
maxy = 0
with open('6-1.txt') as f:
    ch = 'A'
    for line in f:
        m = pat.match(line.strip())
        c = (int(m.group(1)), int(m.group(2)), ch)
        coords.append(c)
        ch = chr(ord(ch) + 1)
        if c[0] < minx:
            minx = c[0]
        if c[0] > maxx:
            maxx = c[0]
        if c[1] < miny:
            miny = c[1]
        if c[1] > maxy:
            maxy = c[1]

print('coords', coords)
print(minx, miny, maxx, maxy)
print('grid', (minx - maxx, miny - maxy), (maxx * 2, maxy * 2))
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

grid = {}

#for x in range(minx - maxx, maxx * 2 + 1):
#    for y in range(miny - maxy, maxy * 2 + 1):
for x in range(-1000, 1000):
    for y in range(-1000, 1000):
        key = str(x) + ',' + str(y)
        grid[key] = (999999, None)
        for c in coords:
            d = manhat_distxy(c, x, y)
            #if key == '4,4':
             #   print(d, c, grid[key])
            if d == grid[key][0]:
                grid[key] = (d, None)
            if d < grid[key][0]:
                grid[key] = (d, c)

infmap = {}
for key, c in grid.items():
    if c is None or c[1] is None:
        continue
    ch = c[1][2]
    d = c[0]
    #print('d', d, 'ch', ch)
    if d > maxdist_map2[ch]:
        infmap[ch] = True

#print(infmap)

totmap = {}
for key, c in grid.items():
    if c is None or c[1] is None:
        continue
    ch = c[1][2]
    if ch in infmap:
        continue
    d = c[0]
    if ch not in totmap:
        totmap[ch] = 0
    totmap[ch] += 1
    #print('coord', key, ch, d)

#print(grid['4,4'])

print(totmap)

maxkey = max(totmap, key=lambda x:totmap[x])
print(maxkey, totmap[maxkey])
