import sys
from collections import defaultdict
sys.setrecursionlimit(5000)

# < 991
depth = 6084
target = '14,709'
target_x = 14
target_y = 709

p = True

#depth = 510
#target_x = 10
#target_y = 10

# this should get 1087
depth = 6969
target_x, target_y = 9, 796

max_x = target_x + 10
max_y = target_y + 10

print(max_x, max_y)

grid = {}
ero_table = {}

def key(x,y):
    return str(x) + ',' + str(y)

def get_type(x,y):
    ero_lev = None
    if (x == 0 and y == 0) or (x == target_x and y == target_y):
        ero_lev = depth % 20183
    elif y == 0:
        ero_lev = (x * 16807 + depth) % 20183
    elif x == 0:
        ero_lev = (y * 48271 + depth) % 20183
    else:
        ero_lev = (ero_table[key(x-1,y)] * ero_table[key(x,y-1)] + depth) % 20183
    ero_table[key(x,y)] = ero_lev
    
    if ero_lev % 3 == 0:
        return '.'
    elif ero_lev % 3 == 1:
        return '='
    elif ero_lev % 3 == 2:
        return '|'

for y in range(0, max_y + 1):
    for x in range(0, max_x + 1):
        grid[key(x,y)] = get_type(x,y)

for y in range(0, max_y):
    for x in range(0, max_x):
        c = grid[key(x,y)]
        if p:
            if x == 0 and y == 0:
                print('M', end='')
            elif x == target_x and y == target_y:
                print('T', end='')
            else:
                print(c, end='')
    if p:
        print()

min_found = 99999999999
best = defaultdict(lambda:999999)

def dfs(x,y,px,py,eq,mins,mvs):
    global min_found

    def manhat_dist(c1, c2):
        return abs(c1 - target_x) + abs(c2 - target_y)

    def checkmark(nx,ny,neq):
        gx = x + nx
        gy = y + ny
        if gx < 0 or gy < 0:
            return 99999999999
        if gx > max_x or gy > max_y:
            return 99999999999
        if px == gx and py == gy:
            return 99999999999
        k = key(gx, gy)
        if gx == target_x and gy == target_y:
            return 1
        if grid[k] == '.' and neq != 'n':
            return manhat_dist(gx, gy)
        elif grid[k] == '=' and neq != 't':
            return manhat_dist(gx, gy)
        elif grid[k] == '|' and neq != 'c':
            return manhat_dist(gx, gy)
        else:
            return 99999999999

    if x == target_x and y == target_y:
        if eq != 't':
            mins += 7

    if mins > min_found:
        return mins

    k = key(x,y)
    if k in mvs:
        return 9999999999

    mvs[k] = mins
    if mins <= best[k]:
        best[k] = mins
    else:
        return 9999999999

    if x == target_x and y == target_y:
        min_found = min(min_found, mins)
        #print(min_found, sum((m[2] for m in mvs)), mvs)
        if min_found == 45:
            for m in mvs:
                print(m)
        print(min_found, mins, len(mvs))
        return mins

    # branch
    m = mins

    eqsw = None
    if eq == 't':
        eqsw = ['t', 'c', 'n']
    elif eq == 'c':
        eqsw = ['c', 't', 'n']
    elif eq == 'n':
        eqsw = ['n', 'c', 't']
    else:
        print(eq)
        exit()

    for sw in eqsw:
        if grid[k] == '.' and sw == 'n':
            continue
        elif grid[k] == '=' and sw == 't':
            continue 
        elif grid[k] == '|' and sw == 'c':
            continue

        mdelt = 1 if eq == sw else 8
        east = checkmark(1,0,sw)
        west = checkmark(-1,0,sw)
        north = checkmark(0, -1,sw)
        south = checkmark(0, 1,sw)

        ordering = sorted( (t for t in [('east', east, 1, 0), ('west', west, -1, 0), ('north', north, 0, -1), ('south', south, 0, 1)] if t[1] < 9999999999), key=lambda x:x[1])

        #if len(ordering) > 0:
            #print(ordering[0][1], m, x, y)

        for i in ordering:
            #nmvs = mvs
            #nmvs = list(mvs)
            nmvs = dict(mvs)
            #nmvs.append((x + i[2], y + i[3], mdelt, sw))
            m = min(m, dfs(x + i[2], y + i[3], x, y, sw, mins + mdelt, nmvs))

    return m

    pass

dfs(0,0,0,0,'t',0,{})
print('best', best[key(target_x, target_y)])