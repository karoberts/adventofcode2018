import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

max_x = 0
max_y = 0

def key(x,y):
    return str(x) + ',' + str(y)

def de_key(k):
    s = k.split(',')
    return (int(s[0]), int(s[1]))

grid = {}

def printit():
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            print(grid[k], end='')
        print()
    print()

with open('18.txt') as f:
    y = 0
    for line in (l.strip('\n') for l in f):
        x = 0
        max_x = len(line)
        for c in line:
            k = key(x,y)
            grid[k] = c
            x += 1
        y += 1
    max_y = y

def check_it(x,y):
    return grid[key(x,y)]

coords = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]

def count(x,y):
    counts = {'.':0, '|':0, '#':0}
    for c in coords:
        k = key(x + c[0], y + c[1])
        if k not in grid:
            continue
        counts[grid[k]] += 1
    return counts

def minute():
    newgrid = {}

    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            cs = count(x, y)

            newgrid[k] = grid[k]
            if grid[k] == '.' and cs['|'] >= 3:
                newgrid[k] = '|'
            elif grid[k] == '|' and cs['#'] >= 3:
                newgrid[k] = '#'
            elif grid[k] == '#' and (cs['#'] < 1 or cs['|'] < 1):
                newgrid[k] = '.'

    return newgrid

def gather():
    woods = 0
    lumber = 0
    for k in grid.keys():
        if grid[k] == '|':
            woods += 1
        elif grid[k] == '#':
            lumber += 1
    return (woods, lumber)

printit()

for m in range(1, 11):
    grid = minute()
    d = gather()
    print(m, d, d[0] * d[1])

printit()

data = gather()

print('part1', data[0] * data[1])

# noticed a repeating 28 digit pattern at minute 896
pats = [205907,207468,208962,210184,211145,211200,205965,201863,201600,202404,204074,205220,209951,211088,214292,214587,216315,214935,214635,213239,211653,203814,204941,204680,203138,204756,206305,204960]

for i in range(896, 1000000001, 28):
    pass
print(i)

print(pats[1_000_000_000 - i])