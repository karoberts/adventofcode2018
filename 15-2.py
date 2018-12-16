def key(x,y):
    return str(x) + ',' + str(y)

def de_key(k):
    s = k.split(',')
    return (int(s[0]), int(s[1]))

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
                elif marks[k] < 10:
                    print(marks[k], end='')
                else:
                    print(marks[k] % 10, end='')
            elif k in elves:
                print('E', end='')
            elif k in goblins:
                print('G', end='')
            else:
                print(grid[k], end='')
        print()
    print()

lees_count = 0
def mark_lees(nx, ny, i, marks, move_locs, targets, friends, min_tgt_dist):
    global lees_count

    #global cur_k

    lees_count += 1

    kn = key(nx, ny)
    if nx < 0 or ny < 0 or nx >= max_x or ny >= max_y or grid[kn] == '#' or kn in friends:
        return False

#   if cur_k:
#       printit_marks(marks)
#       print(min_tgt_dist)
#       wait()

    if kn in targets:
        if i + 1 < min_tgt_dist[0]:
             min_tgt_dist[0] = i + 1
        return True

    if kn in marks and i + 1 >= marks[kn]:
        return False

    if i + 1 > min_tgt_dist[0]:
        return False

    marks[kn] = i + 1

    sk = [False] * 4
    if key(x-2, y) in targets:
        sk[0] = True
        if mark_lees(nx - 1, ny, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
            move_locs[kn] = marks[kn]
    if key(x+2, y) in targets:
        sk[1] = True
        if mark_lees(nx + 1, ny, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
            move_locs[kn] = marks[kn]
    if key(x, y-2) in targets:
        sk[2] = True
        if mark_lees(nx, ny - 1, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
            move_locs[kn] = marks[kn]
    if key(x, y+2) in targets:
        sk[3] = True
        if mark_lees(nx, ny + 1, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
            move_locs[kn] = marks[kn]

    if not sk[0] and mark_lees(nx - 1, ny, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[kn] = marks[kn]
    if not sk[2] and mark_lees(nx, ny - 1, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[kn] = marks[kn]
    if not sk[1] and mark_lees(nx + 1, ny, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[kn] = marks[kn]
    if not sk[3] and mark_lees(nx, ny + 1, i + 1, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[kn] = marks[kn]

    return False

import msvcrt

def wait():
    msvcrt.getch()


cur_k = False
def lees(x, y, targets, friends):
    global rn
    global cur_k

    k = key(x,y)
    i = 0
    marks = {k: i}
    move_locs = {}
    min_tgt_dist = [999999]

#    print('working on', k)
#   if k == '11,14':
#       cur_k = True

    if key(x-1, y) in targets:
        min_tgt_dist[0] = 1
    if key(x+1, y) in targets:
        min_tgt_dist[0] = 1
    if key(x, y-1) in targets:
        min_tgt_dist[0] = 1
    if key(x, y+1) in targets:
        min_tgt_dist[0] = 1

#   if cur_k:
#       print('start lees')
    
    if mark_lees(x - 1, y, i, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[k] = marks[k]
    if mark_lees(x, y - 1, i, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[k] = marks[k]
    if mark_lees(x + 1, y, i, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[k] = marks[k]
    if mark_lees(x, y + 1, i, marks, move_locs, targets, friends, min_tgt_dist):
        move_locs[k] = marks[k]

    #if rn == 24:
#   printit_marks(marks)
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
            enemy['hp'] -= me['pw'] 
            if enemy['hp'] <= 0:
                print(e, 'dies')
                del enemies[e]
            return True
    return False

def round(rn):
    moves = []
    attacked = False
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
                    newpos = de_key(move)
                    attacked |= attack(move, newpos[0], newpos[1], elves[move], goblins)
                else:
                    attacked |= attack(k, x, y, elves[k], goblins)
            elif k in goblins:
                if goblins[k]['lr'] == rn:
                    continue
                move = lees(x,y,elves,goblins)
                goblins[k]['lr'] = rn
                if move:
                    moves.append((k, move, 'G'))
                    goblins[move] = goblins[k]
                    del goblins[k]
                    newpos = de_key(move)
                    attacked |= attack(move, newpos[0], newpos[1], goblins[move], elves)
                else:
                    attacked |= attack(k, x, y, goblins[k], elves)
            else:
                continue
    #print(moves);

    if (not attacked and len(moves) == 0) or len(elves) == 0 or len(goblins) == 0:
        print('DONE', rn)
        return False
    return True

max_x = 0
max_y = 0
# test1 = 27730 pw3   4988  pw15
# test6 = 31284
pw = 4
while True:
    elves = {}
    goblins = {}
    grid = {}

    with open('15.txt') as f:
        y = 0
        for line in (l.strip('\n') for l in f):
            x = 0
            max_x = len(line)
            for c in line:
                k = key(x,y)
                grid[k] = c
                if c == 'E':
                    elves[k] = {'t': 'E', 'hp': 200, 'lr': 0, 'pw': pw}
                    grid[k] = '.'
                elif c == 'G':
                    goblins[k] = {'t': 'G', 'hp': 200, 'lr': 0, 'pw': 3}
                    grid[k] = '.'
                x += 1
            y += 1
        max_y = y

    printit()

    nelves = len(elves)

    next = True
    for rn in range(1, 100):
        print('Round', rn, 'pw', pw)
        next = round(rn)

        if nelves - len(elves) > 0:
            pw += 1
            break

        if not next:
            printit()
            print(elves)
            print(goblins)
            print('elves', [e['hp'] for e in elves.values()])
            print('goblins', [g['hp'] for g in goblins.values()])
            print('combat over')
            print('# deaths:', nelves - len(elves))
            hp = 0
            for g in goblins.values():
                hp += g['hp']
            for e in elves.values():
                hp += e['hp']
            print(rn - 1, (rn - 1) * hp)
            print(rn, rn * hp)
            print('lees', lees_count)
            if nelves - len(elves) == 0:
                exit()
            break

        #printit()
        #print('lees', lees_count)
        #print('elves', [e['hp'] for e in elves.values()])
        #print('goblins', [g['hp'] for g in goblins.values()])
        #print(elves)
        #print(goblins)

