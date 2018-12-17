import re
import sys

# sed 's/\(.\)/\1\n/g' a.txt | sort | uniq -c

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def key(x,y):
    return str(x) + ',' + str(y)

def printit(toscr = True):
    ws = 0
    for y in range(0, max_y + 1):
        for x in range(min_clay_x - 1, max_x + 2):
            if x == 500 and y == 0:
                print('+', end='')
                continue
            k = key(x,y)
            if k in clay:
                if toscr:
                    print('#', end='')
            elif k in water and k in drop:
                if toscr:
                    print('!', end='')
                ws += 1
            elif k in water:
                if toscr:
                    print('~', end='')
                if y >= min_y:
                    ws += 1
            elif k in drop:
                if toscr:
                    print('|', end='')
                if y >= min_y:
                    ws += 1
            else:
                if toscr:
                    print('.', end='')
        if toscr:
            print()
    if toscr:
        print()
    return ws

pat = re.compile(r'^(x|y)=(\d+), (x|y)=(\d+)..(\d+)$')

clay = set()
max_y = 0
min_y = 9999999
max_x = 0
min_clay_x = 9999999
with open('17.txt') as f:
    for line in (l.strip('\n') for l in f):
        m = pat.match(line)
        if m.group(1) == 'x':
            x = int(m.group(2))
            max_x = max(x, max_x)
            min_clay_x = min(x, min_clay_x)
            for y in range(int(m.group(4)), int(m.group(5)) + 1):
                k = key(x,y)
                clay.add(k)
                max_y = max(y, max_y)
                min_y = min(y, min_y)
        else:
            y = int(m.group(2))
            max_y = max(y, max_y)
            min_y = min(y, min_y)
            for x in range(int(m.group(4)), int(m.group(5)) + 1):
                k = key(x,y)
                clay.add(k)
                max_x = max(x, max_x)
                min_clay_x = min(x, min_clay_x)

eprint('mcx', min_clay_x)
eprint('miny', min_y)
eprint('maxcy', max_x, max_y)

# spring = (500, 0)

cur_x = 500
cur_y = 0

water = set()
SENTINEL = -9889898
hitmax = False
deepest = 0

def flow(x, y):
    global hitmax
    global deepest

    k = key(x,y)
    if k in water or k in clay or k in drop:
        return
    deepest = max(y, deepest)
    if y > max_y:
        hitmax = True
        return
    k_dn = key(x, y + 1)
    if k_dn not in clay and k_dn not in water:
        drop.add(k)
        flow(x, y + 1)
    elif k_dn in clay or k_dn in water:
        blk_r = SENTINEL
        drop_r = SENTINEL
        for cx in range(x + 1, max_x + 1):
            k_c = key(cx, y)
            k_c_dn = key(cx, y + 1)
            if k_c_dn not in clay and k_c_dn not in water:
                drop_r = cx
                break
            if k_c in clay or k_c in water:
                blk_r = cx
                break

        blk_l = SENTINEL
        drop_l = SENTINEL
        for cx in range(x, 0, -1):
            k_c = key(cx, y)
            k_c_dn = key(cx, y + 1)
            if k_c_dn not in clay and k_c_dn not in water:
                drop_l = cx
                break
            if k_c in clay or k_c in water:
                blk_l = cx
                break

        if drop_r != SENTINEL and drop_l == SENTINEL:
            for cx in range(x, drop_r):
                k_c = key(cx, y)
                drop.add(k_c)
            for cx in range(blk_l + 1, x):
                k_c = key(cx, y)
                drop.add(k_c)
            flow(drop_r, y)
        elif drop_l != SENTINEL and drop_r == SENTINEL:
            for cx in range(drop_l + 1, x):
                k_c = key(cx, y)
                drop.add(k_c)
            for cx in range(x, blk_r):
                k_c = key(cx, y)
                drop.add(k_c)
            flow(drop_l, y)
        elif blk_l == SENTINEL or blk_r == SENTINEL:
            drop.add(k)
            flow(x + 1, y)
            flow(x - 1, y)
        elif blk_l != SENTINEL and blk_r != SENTINEL:
            for cx in range(blk_l + 1, blk_r):
                k_c = key(cx, y)
                water.add(k_c)
                if k_c in drop:
                    drop.remove(k_c)

sys.setrecursionlimit(2500)

round = 0
last_drop_size = 0
last_water_size = 0
while True:                
    drop = set()
    flow(500, 1)
    if last_drop_size == len(drop) and last_water_size == len(water):
        c = printit(False)
        eprint(c)
        eprint(len(water) + len(drop))
        for w in water:
            if w in drop:
                print('d+w', w)
            if w in clay:
                print('d+c', w)
        for d in drop:
            if d in water:
                print('w+d', d)
            if d in clay:
                print('c+d', d)
        exit()

    last_drop_size = len(drop)
    last_water_size = len(water)
    eprint('round', round, 'deep', deepest)
    #if round == 700:
        #c = printit(True)
        #print(c)
        #exit()
    #if hitmax:
        #break
    round += 1

c = printit(True)

print(c)
#print(len(water) + len(drop))
#print(water)
#print(len(drop))
