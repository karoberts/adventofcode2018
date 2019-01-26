import re

def addcart(x,y,k,dir):
    cart = {'id': len(carts), 'dir': dir, 'x': x, 'y': y, 'tc': 1}
    carts.append(cart)
    cartpos[k] = cart

pat = re.compile(r'^$')

grid = {}
carts = []
cartpos = {}
with open('13.txt') as f:
    y = 0
    for line in (l.strip('\n') for l in f):
        x = 0
        for c in line:
            k = (x,y)
            if c == '-':
                grid[k] = 'hz'
            elif c == '|':
                grid[k] = 'vt'
            elif c == '/':
                grid[k] = 'br_tl'
            elif c == '\\':
                grid[k] = 'bl_tr'
            elif c == '+':
                grid[k] = 'int'
            elif c == '^':
                addcart(x,y,k,'U')
                grid[k] = 'vt'
            elif c == 'v':
                addcart(x,y,k,'D')
                grid[k] = 'vt'
            elif c == '<':
                addcart(x,y,k,'L')
                grid[k] = 'hz'
            elif c == '>':
                addcart(x,y,k,'R')
                grid[k] = 'hz'
            elif c == ' ':
                pass
            else:
                raise 'bad char ' + k

            x += 1
        y += 1

#print(grid)

def turncart(cart):
    if cart['tc'] == 1:
        if cart['dir'] == 'U':
            cart['dir'] = 'L'
        elif cart['dir'] == 'D':
            cart['dir'] = 'R'
        elif cart['dir'] == 'R':
            cart['dir'] = 'U'
        elif cart['dir'] == 'L':
            cart['dir'] = 'D'
        cart['tc'] = 2
    elif cart['tc'] == 2:
        cart['tc'] = 3
    elif cart['tc'] == 3:
        if cart['dir'] == 'U':
            cart['dir'] = 'R'
        elif cart['dir'] == 'D':
            cart['dir'] = 'L'
        elif cart['dir'] == 'R':
            cart['dir'] = 'D'
        elif cart['dir'] == 'L':
            cart['dir'] = 'U'
        cart['tc'] = 1

def movecart(x,y,k):
    cart = cartpos[k]
    if cart['dir'] == 'U':
        next = (x, y-1)
        track = grid[next]
        if track == 'br_tl':
            cart['dir'] = 'R'
        elif track == 'bl_tr':
            cart['dir'] = 'L'
        elif track == 'int':
            turncart(cart)
        cart_moves.append((cart, next, k))
        pass
    elif cart['dir'] == 'D':
        next = (x, y+1)
        track = grid[next]
        if track == 'br_tl':
            cart['dir'] = 'L'
        elif track == 'bl_tr':
            cart['dir'] = 'R'
        elif track == 'int':
            turncart(cart)
        cart_moves.append((cart, next, k))
    elif cart['dir'] == 'R':
        next = (x+1, y)
        track = grid[next]
        if track == 'br_tl':
            cart['dir'] = 'U'
        elif track == 'bl_tr':
            cart['dir'] = 'D'
        elif track == 'int':
            turncart(cart)
        cart_moves.append((cart, next, k))
    elif cart['dir'] == 'L':
        next = (x-1, y)
        track = grid[next]
        if track == 'br_tl':
            cart['dir'] = 'D'
        elif track == 'bl_tr':
            cart['dir'] = 'U'
        elif track == 'int':
            turncart(cart)
        cart_moves.append((cart, next, k))

part = 2
 
tick = 0
while True:
    #if tick % 100 == 0:
    #    print(tick, len(cartpos))
    cart_moves = []
    carts_removed = set()
    for y in range(0, 150):
        for x in range(0, 150):
            k = (x,y)
            if k in cartpos:
                movecart(x,y,k)

    for cm in cart_moves:
        cart = cm[0]
        next = cm[1]
        k = cm[2]
        if k in carts_removed:
            continue
        if next in cartpos:
            print('collision! at', next)
            if part == 1:
                quit()
            print('removing carts at', k, next)
            del cartpos[k]
            del cartpos[next]
            carts_removed.add(next)
        else:
            #print('moving cart from', k, 'to', next)
            cartpos[next] = cart
            del cartpos[k]

    if len(cartpos) == 1:
        print('part 2: last cart at', cartpos)
        quit()

    tick += 1
