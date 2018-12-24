import re
import sys
import dllist
import heapq
import json
from collections import defaultdict

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def key(x,y):
    return str(x) + ',' + str(y)

with open('20.txt') as f:
    line = f.readline().strip()

def printit(qs = False, marks = None):
    for y in range(min_y - 2, max_y + 3):
        for x in range(min_x - 2, max_x + 3):
            k = key(x,y)
            if marks and k in marks:
                print(str(marks[k] % 10), end='')
            elif k not in grid:
                print(' ', end='')
            elif not qs and grid[k] == '?':
                print('#', end='')
            else:
                print(grid[k], end='')
        print()

#line = '^WNE$'
#line = '^ENWWW(NEEE|SSE(EE|N))$'   # 10
#line = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'  # 18
#line = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'  # 23
#line = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'   # 31

def index_parens():
    stack = []
    prevpipe = []
    for p, c in enumerate(line):
        if c == '(':
            stack.append((p,c,[]))
            prevpipe.append(p)
        elif c == '|':
            pc = stack[-1]
            pc[2].append(p)
            pp = prevpipe.pop()
            pipemap[pp] = (p, c)
            prevpipe.append(p)
        elif c == ')':
            pc = stack.pop()
            parenmap[pc[0]] = p
            for i in pc[2]:
                parenmap[i] = p
            pp = prevpipe.pop()
            pipemap[pp] = (p, c)

pat = re.compile(r'(EW|WE|NS|SN)')
pat2 = re.compile(r'(\(\|\))')
def remove_noops(l):
    a = re.sub(pat, '', l)
    if a is None:
        a = l
    b = re.sub(pat2, '', a)
    if b is None:
        b = l
    return b


# doing this produces the wrong answer
#ln = len(line)
#print(len(line))
#line = remove_noops(line)
##print(line)
#while len(line) < ln:
#    ln = len(line)
#    line = remove_noops(line)
#    #print(line)
#print(line)
#print(len(line))
##exit()

dist = defaultdict(lambda :999999999)
prev = {}

def dijkstra():
    global pipemap

    def get_neighbors(uk, x, y, pos):
        if line[pos] == 'W': return [(1, key(x-2, y), x-2, y, pos + 1)]
        elif line[pos] == 'E': return [(1, key(x+2, y), x+2, y, pos + 1)]
        elif line[pos] == 'N': return [(1, key(x, y-2), x, y-2, pos + 1)]
        elif line[pos] == 'S': return [(1, key(x, y+2), x, y+2, pos + 1)]
        return []

    def addit(u, n):
        entry = [dist[u[1]], n[1], n[2], n[3], n[4], True]
        finder[n[1]] = entry

        heapq.heappush(h, entry)

    dist['0,0'] = 0
    prev['0,0'] = None

    finder = {}

    inq = set()
    h = []
    heapq.heappush(h, [0, '0,0', 0, 0, 1, True])
    finder['0,0'] = h[0]
    inq.add('0,0')

    while len(h) > 0:
        #print_map(dist);
        u = heapq.heappop(h)
        if not u[5]:
            continue
        uk = u[1]
        x = u[2]
        y = u[3]
        pos = u[4]

        if line[pos] == '$':
            continue
        elif line[pos] == '(':
            addit(u, (0, uk, x, y, pos + 1))

            np = pipemap[pos][0]
            while True:
                addit(u, (0, uk, x, y, np + 1))
                pm = pipemap[np]
                if pm[1] == ')':
                    break
                np = pm[0]
            continue
        elif line[pos] == '|':
            addit(u, (0, uk, x, y, parenmap[pos] + 1))
            continue
        elif line[pos] == ')':
            addit(u, (0, uk, x, y, pos + 1))
            continue

        for v in get_neighbors(uk, x, y, pos):
            alt = dist[u[1]] + v[0]
            if alt < dist[v[1]] or v[0] == 0:
                dist[v[1]] = alt
                prev[v[1]] = v[1]
                addit(u, v)

parenmap = {}
pipemap = {}
index_parens()

dijkstra()

#print(json.dumps(dist, indent=2))

maxroom = max(dist, key=lambda x:dist[x])
print('part1', maxroom, dist[maxroom]) 

c = 0
for r in dist:
    if dist[r] >= 1000:
        c += 1
print('part2', c)