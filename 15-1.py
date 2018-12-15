def key(x,y):
    return str(x) + ',' + str(y)

elves = {}
goblins = {}
grid = {}

def printit():
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            if k in elves:
                print('E', end='')
            elif k in goblins:
                print('G', end='')
            else:
                print(grid[k], end='')
        print()
    print()

def printit_marks(marks):
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            if k in marks:
                if marks[k] == 0:
                    if k in elves:
                        print('e', end='')
                    elif k in goblins:
                        print('g', end='')
                else:
                    print(marks[k], end='')
            elif k in elves:
                print('E', end='')
            elif k in goblins:
                print('G', end='')
            else:
                print(grid[k], end='')
        print()
    print()

def mark_lees(nx, ny, i, marks, move_locs, targets, friends):
    kn = key(nx, ny)
    if nx < 0 or ny < 0 or nx >= max_x or ny >= max_y or grid[kn] == '#' or kn in friends:
        return False

    if kn in targets:
        return True

    if kn in marks and i + 1 > marks[kn]:
        return False

    marks[kn] = i + 1

    if mark_lees(nx - 1, ny, i + 1, marks, move_locs, targets, friends):
        move_locs[kn] = marks[kn]
    if mark_lees(nx, ny - 1, i + 1, marks, move_locs, targets, friends):
        move_locs[kn] = marks[kn]
    if mark_lees(nx + 1, ny, i + 1, marks, move_locs, targets, friends):
        move_locs[kn] = marks[kn]
    if mark_lees(nx, ny + 1, i + 1, marks, move_locs, targets, friends):
        move_locs[kn] = marks[kn]

    return False

def lees(x, y, targets, friends):
    global rn

    k = key(x,y)
    i = 0
    marks = {k: i}
    move_locs = {}
    
    if mark_lees(x - 1, y, i, marks, move_locs, targets, friends):
        move_locs[k] = marks[k]
    if mark_lees(x, y - 1, i, marks, move_locs, targets, friends):
        move_locs[k] = marks[k]
    if mark_lees(x + 1, y, i, marks, move_locs, targets, friends):
        move_locs[k] = marks[k]
    if mark_lees(x, y + 1, i, marks, move_locs, targets, friends):
        move_locs[k] = marks[k]

    #if rn == 24:
    #    printit_marks(marks)
    #    print(move_locs)

    if len(move_locs) == 0:
        return None

    mindistkey = min(move_locs, key=lambda x:move_locs[x])
    mindist = move_locs[mindistkey]

    if mindist == 0:
        #print(k, 'not moving')
        return None

    target = None
    for ym in range(0, max_y):
        for xm in range(0, max_x):
            km = key(xm,ym)
            curdist = mindist
            if km in move_locs and move_locs[km] == mindist:
                ymn = ym
                xmn = xm
                while km != k:
                    if curdist == 1:
                        return km
                    curdist -= 1
                    k_up = key(xmn, ymn-1)
                    if k_up in marks and marks[k_up] == curdist:
                        km = k_up
                        ymn -= 1
                    else:
                       k_lf = key(xmn - 1, ymn)
                       if k_lf in marks and marks[k_lf] == curdist:
                           km = k_lf
                           xmn -= 1
                       else:
                           k_rt = key(xmn + 1, ymn)
                           if k_rt in marks and marks[k_rt] == curdist:
                               km = k_rt
                               xmn += 1
                           else:
                               k_dn = key(xmn, ymn + 1)
                               if k_dn in marks and marks[k_dn] == curdist:
                                   km = k_dn
                                   ymn += 1

        if target is not None:
            #printit_marks(marks)
            break

    return target
    #print(k, 'target', target, marks[target])

def attack(k, x, y, me, enemies):
    es = []

    k_up = key(x, y - 1)
    if k_up in enemies:
        es.append(k_up)
    k_lf = key(x - 1, y)
    if k_lf in enemies:
        es.append(k_lf)
    k_rt = key(x + 1, y)
    if k_rt in enemies:
        es.append(k_rt)
    k_dn = key(x, y + 1)
    if k_dn in enemies:
        es.append(k_dn)

    if len(es) == 0:
        return False

    minhp_enemy = min(es, key=lambda x:enemies[x]['hp'])
    minhp = enemies[minhp_enemy]['hp']
    for e in es:
        enemy = enemies[e]
        if enemy['hp'] == minhp:
            enemy['hp'] -= 3
            if enemy['hp'] <= 0:
                print(e, 'dies')
                del enemies[e]
            return True
    return False

def round(rn):
    moves = []
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            if k in elves:
                if elves[k]['lr'] == rn:
                    continue
                move = lees(x,y,goblins,elves)
                elves[k]['lr'] = rn
                if move:
                    moves.append((k, move, 'E'))
                    elves[move] = elves[k]
                    del elves[k]
            elif k in goblins:
                if goblins[k]['lr'] == rn:
                    continue
                move = lees(x,y,elves,goblins)
                goblins[k]['lr'] = rn
                if move:
                    moves.append((k, move, 'G'))
                    goblins[move] = goblins[k]
                    del goblins[k]
            else:
                continue
    #print(moves);

    attacked = False
    for y in range(0, max_y):
        for x in range(0, max_x):
            k = key(x,y)
            if k in elves:
                attacked |= attack(k, x, y, elves[k], goblins)
            elif k in goblins:
                attacked |= attack(k, x, y, goblins[k], elves)
            else:
                continue

    if (not attacked and len(moves) == 0) or len(elves) == 0 or len(goblins) == 0:
        print('DONE', rn)
        return False
    return True

max_x = 0
max_y = 0
with open('15-test5.txt') as f:
    y = 0
    for line in (l.strip('\n') for l in f):
        x = 0
        max_x = len(line)
        for c in line:
            k = key(x,y)
            grid[k] = c
            if c == 'E':
                elves[k] = {'t': 'E', 'hp': 200, 'lr': 0}
                grid[k] = '.'
            elif c == 'G':
                goblins[k] = {'t': 'G', 'hp': 200, 'lr': 0}
                grid[k] = '.'
            x += 1
        y += 1
    max_y = y

printit()

next = True
for rn in range(1, 100):
    print('Round', rn)
    next = round(rn)

    if not next:
        printit()
        print(elves)
        print(goblins)
        print('combat over')
        hp = 0
        for g in goblins.values():
            hp += g['hp']
        for e in elves.values():
            hp += e['hp']
        print((rn - 1) * hp)
        break

    #if rn == 24:
    printit()
    #print(elves)
    #print(goblins)

