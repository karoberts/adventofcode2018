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

def skip_branches(pos):
    parenstack = 0
    while True:
        if line[pos] == '$':
            raise 1
        elif line[pos] == '(':
            parenstack += 1
        elif line[pos] == ')':
            if parenstack == 0:
                return pos + 1
            parenstack -= 1
        pos += 1

def recur5(pos, x, y, depth):
    print(' ' * depth, pos)
    while pos < len(line):
        if line[pos] in ['W', 'N', 'E', 'S']:
            (x, y) = set_door(x, y, line[pos])
            pos += 1
        elif line[pos] == '$':
            return
        elif line[pos] == '(':
            recur5(pos + 1, x, y, depth + 1)
            np = next_branch(pos + 1)
            while np > 0:
                recur5(np + 1, x, y, depth + 1)
                np = next_branch(np + 1)
            pos = -1 * np + 1
        elif line[pos] == '|':
            pos = skip_branches(pos)
        elif line[pos] == ')':
            pos += 1

grid['0,0'] = 'X'
grid['1,0'] = '?'
grid['0,1'] = '?'
grid['-1,0'] = '?'
grid['0,-1'] = '?'
grid['1,1'] = '#'
grid['-1,1'] = '#'
grid['-1,-1'] = '#'
grid['1,-1'] = '#'
recur5(1, 0, 0, 1)

printit()