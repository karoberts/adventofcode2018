import sys

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

line = '^ENWWW(NEEE|SSE(EE|N))$'   # 10
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


from collections import defaultdict

class Node(object):
    __slots__ = ('__value', '__ptrs')

    def __init__(self):
        self.__ptrs = []
        self.__value = ''

    def add_child(self, node):
        self.__ptrs.append(node)

    def get_children(self):
        return self.__ptrs

    def get_value(self):
        return self.__value

    def append_value(self, c):
        self.__value += c

    def __str__(self):
        if len(self.__ptrs) == 0:
            return 'node(' + str(self.__value) + ')'
        return 'node(' + str(self.__value) + '[' + ','.join((str(s) for s in self.__ptrs)) + '])'

    def __repr__(self):
        return '<node(' + str(self.__value) + '[' + ','.join((str(s) for s in self.__ptrs)) + '])>'

    def printit(self):
        self.__printit(self, 0)

    def __printit(self, n, d):
        print('  ' * d, 'node(' + str(n.__value) + ')')
        for c in n.__ptrs:
            self.__printit(c, d + 1)

def recur3(pos, parent):
    newNode = True
    lastPipe = False
    node = None
    while True:
        if line[pos] in ['W', 'N', 'E', 'S']:
            if newNode:
                node = Node()
                parent.add_child(node)
                newNode = False
                lastPipe = False
            node.append_value(line[pos])
            pos += 1
        elif line[pos] == '$':
            return 0
        elif line[pos] == '|':
            newNode = True
            lastPipe = True
            pos += 1
        elif line[pos] == '(':
            pos = recur3(pos + 1, node)
            newNode = True
            lastPipe = False
        elif line[pos] == ')':
            if lastPipe:
                node = Node()
                parent.add_child(node)
            return pos + 1

def recur5(pos, parent):
    newNode = True
    lastPipe = False
    node = None
    while True:
        if line[pos] in ['W', 'N', 'E', 'S']:
            if newNode:
                node = Node()
                parent.add_child(node)
                newNode = False
                lastPipe = False
            node.append_value(line[pos])
            pos += 1
        elif line[pos] == '$':
            return 0
        elif line[pos] == '|':
            newNode = True
            lastPipe = True
            pos += 1
        elif line[pos] == '(':
            pos = recur3(pos + 1, node)
            newNode = True
            lastPipe = False
        elif line[pos] == ')':
            if lastPipe:
                node = Node()
                parent.add_child(node)
            return pos + 1


grid['0,0'] = 'X'
grid['1,0'] = '?'
grid['0,1'] = '?'
grid['-1,0'] = '?'
grid['0,-1'] = '?'
grid['1,1'] = '#'
grid['-1,1'] = '#'
grid['-1,-1'] = '#'
grid['1,-1'] = '#'
#recur2(1, 0, 0)


graph = Node()
#recur3(1, graph)
recur4(1, graph)

graph.printit()