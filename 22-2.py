import sys
from collections import defaultdict
import heapq
sys.setrecursionlimit(5000)

# < 991
depth = 6084
target_x = 14
target_y = 709

p = False

#depth = 510
#target_x = 10
#target_y = 10

# this should get 1087
#depth = 6969
#target_x, target_y = 9, 796

max_x = target_x + 30
max_y = target_y + 30

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
                print('m', end='')
            elif x == target_x and y == target_y:
                print('t', end='')
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

def print_map(dist):
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            c = grid[k]
            if k in dist:
                print(' {:02} '.format(dist[k]), end='')
            elif x == 0 and y == 0:
                print(' mm ', end='')
            elif x == target_x and y == target_y:
                print(' tt ', end='')
            else:
                print(' ' + c + c + ' ', end='')
        print()
    print()

gomap = { '.=' : 'c', '.|': 't', '=.': 'c', '=|': 'n', '|.': 't', '|=': 'n' }

def dijkstra():
    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    def get_neighbors(x,y,eq):
        k = key(x,y)
        c = grid[k]
        ns = []

        for t in tests:
            tx = x + t[0]
            ty = y + t[1]
            if tx < 0 or ty < 0 or tx >= max_x or ty >= max_y:
                continue
            tk = key(tx, ty)
            tt = grid[tk]

            if tt == c:
                ns.append( [1, tx, ty, tk + ',' + eq, eq] )
                continue

            needed_tool = gomap[c + tt]
            if eq == needed_tool:
                ns.append( [1, tx, ty, tk + ',' + eq, eq] )
            else:
                ns.append( [8, tx, ty, tk + ',' + needed_tool, needed_tool] )

        for n in ns:
            n.append(True)
        return ns

    dist['0,0,t'] = 0

    prev['0,0,t'] = None

    finder = {}

    inq = set()
    h = []
    heapq.heappush(h, [0, 0, 0, '0,0,t', 't', True])
    finder['0,0,t'] = h[0]
    inq.add('0,0,t')

    while len(h) > 0:
        #print_map(dist);
        u = heapq.heappop(h)
        if not u[5]:
            continue
        inq.remove(u[3])
        #if u[1] == target_y and u[2] == target_y:
            #return u
        uk = u[3]
        for v in get_neighbors(u[1], u[2], u[4]):
            if v[1] == target_x and v[2] == target_y:
                if v[4] != 't' and v[0] == 1:
                    v[0] += 7
                    v[4] = 't'
                    v[3] = key(target_x, target_y) + ',t'
            alt = dist[uk] + v[0]
            if alt < dist[v[3]]:
                dist[v[3]] = alt
                prev[v[3]] = (uk, v[0], v[4], v[1], v[2])
                entry = [alt, v[1], v[2], v[3], v[4], True]
                if v[3] in inq:
                    finder[v[3]][5] = False
                inq.add(v[3])
                finder[v[3]] = entry

                heapq.heappush(h, entry)

def print_path(tgt):
    s = []
    u = (tgt + ',t', 0, 't')
    cost = 0
    while u:
        s.append(u)
        cost += u[1]
        u = prev[u[0]] if u[0] in prev else None

    #for c in reversed(s):
     #   print(c[0], c[1], grid[key(c[3], c[4])], c[2])
    return cost


#dfs(0,0,0,0,'t',0,{})
#print('best', best[key(target_x, target_y)])

prev = {}
dist = defaultdict(lambda :999999999)

x = dijkstra()
#print(x)

cost = print_path(key(target_x, target_y))
#print(dist[key(target_x, target_y) + ',t'])
print('part2',cost)

#cost = print_path(key(4,4))
#print(cost)
