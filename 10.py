import json
import re
import math
#import msvcrt

#def wait():
#    msvcrt.getch()

def in_seq(x, ys):
    seq = 0
    for i, y in enumerate(sorted(ys)):
        if i == 0:
            st = y + 1
            continue
        if y == st:
            seq += 1
            st += 1
            continue
        if seq > 2:
            print('found', sec, x)
            print([str(p['x']) + ',' + str(p['y']) + "N" for p in points])
        return False
    return True

def dist(p1, p2):
    return math.sqrt(abs(p1['x'] - p2['x'])**2 + abs(p1['y'] - p2['y'])**2)

def has_msg():
    #minx = min(points, key=lambda x:x['x']) ['x']
    #maxx = max(points, key=lambda x:x['x']) ['x']
    #miny = min(points, key=lambda x:x['y']) ['y']
    #maxy = max(points, key=lambda x:x['y']) ['y']

    cols = {}
    pts_under = 0
    for p1 in points:
        for p2 in points:
            if dist(p1, p2) < 5:
                pts_under += 1
        break

    return pts_under > 40

    #cols = {k: sorted(v) for k, v in cols.items() if len(v) > 3 and in_seq(k, v)}
    #if len(cols) > 0:
        #print(cols)
        #return True
    #return False

def print_it(s):
    with open('csv10-' + str(s) + '.csv', 'w') as o:
        for p in points:
            o.write(str(p['x']) + ',' + str(p['y']) + "\n")

pat = re.compile(r'^position=<[ ]*([\-\d]+),[ ]*([\-\d]+)> velocity=<[ ]*([\-\d]+),[ ]*([\-\d]+)>$')

#print(in_seq([5,4,7,6,3,8]))

# 505,605

points = []
with open('10.txt') as f:
    for line in (l.strip() for l in f):
        #print(line)
        m = pat.match(line)
        points.append({'x':int(m.group(1)), 'y': int(m.group(2)), 'dx':int(m.group(3)), 'dy':int(m.group(4))})

"""
for i, p in enumerate(points):
    p['x'] += p['dx'] * 8000
    p['y'] += p['dy'] * 8000
"""

for sec in range(1, 15000):
    for i, p in enumerate(points):
        ox = p['x']
        oy = p['y']
        p['x'] += p['dx']
        p['y'] += p['dy']
        #if (ox < 0 and p['x'] > 0) or (ox > 0 and p['x'] < 0) or (oy < 0 and p['y'] > 0) or (oy > 0 and p['y'] < 0):
            #print(sec, 'point', p, 'switched')

    #if sec % 100 == 0:
        #print(sec)

    #if sec % 1000 == 0:
        #print_it(sec)

    if has_msg():
        # plot in excel, flip the Y axis
        print_it(sec)
        break
