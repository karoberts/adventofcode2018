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

def manhat_totdist(cs, x, y):
    totdist = 0
    for c in cs:
        totdist += manhat_distxy(c, x, y)
    return totdist

pat = re.compile(r'^([\-\d]+),[ ]?([\-\d]+)$')
coords = []
minx = 999999999
maxx = 0
miny = 999999999
maxy = 0
with open('06-1.txt') as f:
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

grid = {}

print(manhat_totdist(coords, 4, 3))

for x in range(int((minx - maxx) / 3), maxx + 1):
    for y in range(int((miny - maxy) / 3), maxy + 1):
        totdist = manhat_totdist(coords, x, y)
        if totdist < 10000:
            grid[str(x) + ',' + str(y)] = totdist

#print(grid)
print(len(grid))
