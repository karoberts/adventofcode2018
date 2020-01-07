
depth = 6084
target = '14,709'
target_x = 14
target_y = 709

p = False

#depth = 510
#target_x = 10
#target_y = 10

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

for y in range(0, target_y + 10):
    for x in range(0, target_x + 10):
        grid[key(x,y)] = get_type(x,y)

risk = 0
for y in range(0, target_y + 10):
    for x in range(0, target_x + 10):
        c = grid[key(x,y)]
        if p:
            if x == 0 and y == 0:
                print('M', end='')
            elif x == target_x and y == target_y:
                print('T', end='')
            else:
                print(c, end='')
        if x <= target_x and y <= target_y:
            if c == '=':
                risk += 1
            elif c == '|':
                risk += 2
    if p:
        print()
print(risk)
