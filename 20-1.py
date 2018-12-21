import re
import sys
import dllist

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def key(x,y):
    return str(x) + ',' + str(y)

with open('20.txt') as f:
    line = f.readline().strip()


def printit(qs = False):
    for y in range(min_y - 2, max_y + 3):
        for x in range(min_x - 2, max_x + 3):
            k = key(x,y)
            if k not in grid:
                print(' ', end='')
            elif not qs and grid[k] == '?':
                print('#', end='')
            else:
                print(grid[k], end='')
        print()

#line = '^ENWWW(NEEE|SSE(EE|N))$'   # 10
#line = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'  # 18
#line = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'  # 23
#line = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'   # 31

grid = {}
min_x = 99999999999999
min_y = 99999999999999
max_x = -99999999999999
max_y = -99999999999999

def set_grid(nx, ny, c):
    k = key(nx, ny)
    if k in grid and grid[k] != '?':
        return
    grid[k] = c

def set_door(x, y, c):
    global min_x
    global min_y
    global max_x
    global max_y
    min_x = min(min_x, x - 2)
    min_y = min(min_y, y - 2)
    max_x = max(max_x, x + 2)
    max_y = max(max_y, y + 2)

    if c == 'E':
        set_grid(x + 1,y, '|')
        set_grid(x + 2,y, '.')
        set_grid(x + 1,y - 1, '#')
        set_grid(x + 1,y + 1, '#')
        set_grid(x + 2,y - 1, '?')
        set_grid(x + 2,y + 1, '?')
        set_grid(x + 3,y, '?')
        return (x + 2, y)
    elif c == 'W':
        set_grid(x - 1,y, '|')
        set_grid(x - 2,y, '.')
        set_grid(x - 1,y - 1, '#')
        set_grid(x - 1,y + 1, '#')
        set_grid(x - 2,y - 1, '?')
        set_grid(x - 2,y + 1, '?')
        set_grid(x - 3,y, '?')
        return (x - 2, y)
    elif c == 'N':
        set_grid(x,y - 1, '-')
        set_grid(x,y - 2, '.')
        set_grid(x - 1,y - 1, '#')
        set_grid(x + 1,y - 1, '#')
        set_grid(x - 1,y - 2, '?')
        set_grid(x + 1,y - 2, '?')
        set_grid(x,y - 3, '?')
        return (x, y - 2)
    elif c == 'S':
        set_grid(x,y + 1, '-')
        set_grid(x,y + 2, '.')
        set_grid(x - 1,y + 1, '#')
        set_grid(x + 1,y + 1, '#')
        set_grid(x - 1,y + 2, '?')
        set_grid(x + 1,y + 2, '?')
        set_grid(x,y + 3, '?')
        return (x, y + 2)

def next_branch(pos):
    parenstack = 0
    while True:
        if line[pos] == '$':
            raise 1
        elif line[pos] == '(':
            parenstack += 1
        elif line[pos] == ')':
            if parenstack == 0:
                return pos * -1
            parenstack -= 1
        elif line[pos] == '|' and parenstack == 0:
            return pos
        pos += 1

class Node(object):
    def __init__(self, pos, x, y, px, py, parens, skipping):
        self.pos = pos
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.parens = parens
        self.skipping = skipping

    def __str__(self):
        return "Node(pos {}, ({}, {}), ({}, {}) ps {}, sk={})".format(self.pos, self.x, self.y, self.px, self.py, self.parens, self.skipping)

    def __repr__(self):
        return '<' + str(self) + '>'

def recur6(q):
    while len(q) > 0:
        track = q.popleft()

        pos = track.pos
        x = track.x
        y = track.y
        while True:
            if not track.skipping and line[pos] in ['W', 'N', 'E', 'S']:
                (x, y) = set_door(x, y, line[pos])
            elif line[pos] == '$':
                break
            elif line[pos] == '(':
                if track.skipping:
                    track.parens += 1
                else:
                    q.appendright(Node(pos + 1, x, y, x, y, 1, False))
                break
            elif not track.skipping and line[pos] == '|':
                q.appendright(Node(pos + 1, x, y, track.px, track.py, 1, True))
                q.appendright(Node(pos + 1, x, y, track.px, track.py, 1, False))
                break
            elif line[pos] == ')':
                track.parens -= 1
                if track.parens == 0:
                    track.pos = pos + 1
                    track.skipping = False
                    q.appendright(track)
                break
            pos += 1

def recur5(pos, x, y, depth):
    # print(' ' * depth, pos)
    loops = 0
    np = 0
    while pos < len(line):
        if line[pos] in ['W', 'N', 'E', 'S']:
            (x, y) = set_door(x, y, line[pos])
            pos += 1
        elif line[pos] == '$':
            return loops
        elif line[pos] == '(':
            loops += recur5(pos + 1, x, y, depth + 1)
            np = pipemap[pos][0]
            while True:
                loops += recur5(np + 1, x, y, depth + 1)
                pm = pipemap[np]
                if pm[1] == ')':
                    break
                np = pm[0]
            pos = np
        elif line[pos] == '|':
            pos = parenmap[pos] + 1
        elif line[pos] == ')':
            pos += 1
        loops += 1
    return loops

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


ln = len(line)
print(len(line))
line = remove_noops(line)
#print(line)
while len(line) < ln:
    ln = len(line)
    line = remove_noops(line)
    #print(line)
print(line)
print(len(line))
#exit()


grid['0,0'] = 'X'
grid['1,0'] = '?'
grid['0,1'] = '?'
grid['-1,0'] = '?'
grid['0,-1'] = '?'
grid['1,1'] = '#'
grid['-1,1'] = '#'
grid['-1,-1'] = '#'
grid['1,-1'] = '#'
#q = dllist.dllist()
#q.appendright(Node(1, 0, 0, 0, 0, 0, False))
#recur6(q)

parenmap = {}
pipemap = {}
index_parens()
#print(parenmap)
#print(pipemap)

loops = recur5(1, 0, 0, 0)

print('loops', loops)
printit()
