import re
import sys
from collections import defaultdict
sys.setrecursionlimit(5000)

# pos=<26276148,18772321,-169986>, r=84817629

def manhat_dist_bs(b1, b2):
    return abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])

def manhat_dist_b(b1, x,y,z):
    return abs(b1[0] - x) + abs(b1[1] - y) + abs(b1[2] - z)

def manhat_dist(x1,y1,z1,x2,y2,z2):
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def count_in_range(x,y,z):
    c = 0
    for b in bots:
        d = manhat_dist_b(b, x,y,z)
        if d <= b[3]:
            c += 1
    return c

pat = re.compile(r'^pos=<([\-\d]+),([\-\d]+),([\-\d]+)>, r=([\d]+)$')

bots = []
i = 0
avg = [0, 0, 0]
with open('23.txt') as f:
    for line in (l.strip() for l in f):
        #print(line)
        m = pat.match(line)
        bots.append([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), i])
        i += 1

min_x, min_y, min_z = 99999999, 99999999, 99999999
max_x, max_y, max_z = 0, 0, 0
c = 0
for b in bots:
    min_x = min(min_x, b[0] - b[3])
    max_x = max(max_x, b[0] + b[3])
    min_y = min(min_y, b[1] - b[3])
    max_y = max(max_y, b[1] + b[3])
    min_z = min(min_z, b[2] - b[3])
    max_z = max(max_z, b[2] + b[3])

print('min', min_x, min_y, min_z)
print('max', max_x, max_y, max_z)

# 949  21131263  41496634  56778443
tgt = (21131263, 41496634, 56778443)

for b in bots:
    d = manhat_dist_b(b, tgt[0], tgt[1], tgt[2])
    if d > b[3] and d - b[3] < 1_400_000:
        print(d - b[3], b)

print(count_in_range(tgt[0], tgt[1], tgt[2]))
print(manhat_dist(0, 0, 0, tgt[0], tgt[1], tgt[2]))

mx = 0
for x in range(tgt[0]-1, tgt[0]+ 3):
    for y in range(tgt[1]-10, tgt[1]+10):
        #print(x,y)
        for z in range(tgt[2]-10, tgt[2]+10):
            c = count_in_range(x, y, z)
            if c == 949:
                mx = c
                print(mx, x,y,z, manhat_dist(0,0,0,x,y,z))
                break
                
exit()

# min/max
# -154355239 -154355239 -154355239
# 228637767 228637767 228637767

def next_coords(lx, ly, lz, rx, ry, rz):
    nx = abs(lx - rx) // 2 + rx
    ny = abs(ly - ry) // 2 + ry
    nz = abs(lz - rz) // 2 + rz
    return nx,ny,nz

# 631  37141264 37141264 37141264
# print(count_in_range(40241264,40241264,40241264)) # 735
# 834 [(26587855, 48753774, 52988263)]
# (24376473, 44307494, 56406868) 878 4 552845 444628 369544

# 24376473, 44307494, 56406868) 878 4 552845 444628 369544
# 23823628, 44218566, 56748724) 873 550 55284 44462 36954
# 23768344, 44174104, 56711770) 873 1089 5528 4446 3695
# 23762816, 44169658, 56708075) 873 1089 552 444 369
# 23762264, 44169214, 56707706) 873 1320 55 44 36

# (23788325, 44153794, 56778344) 898
# (22788320, 43153789, 56778344) 902
# (22288320, 42653789, 56778344) 910
# (21788320, 42153789, 56778344) 913

# 2657056 (21131264, 41496733, 56778344) 947

# < 119406341

print(manhat_dist(0, 0, 0, 21131264, 41496733, 56778344))
exit()

#print(count_in_range(23788325, 44153794, 56778344))
# 1897476 (21890844, 42256313, 56778344)
n = 1700000
max = 913
for n in range(2_600_000, 2_900_000):
    c = count_in_range(23788320 - n, 44153789 - n, 56778344)
    if c > max:
        print(n, (23788320 - n, 44153789 - n, 56778344), c)
        max = c
    if c < max:
        print(n, (23788320 - n, 44153789 - n, 56778344), c)
        break
    if n % 10000 == 0:
        print(n)
exit()

def go(min_x, min_y, min_z, max_x, max_y, max_z):
    best = defaultdict(list)
    max_c = 0
    rx = max(1, abs(max_x - min_x) // 10)
    ry = max(1, abs(max_y - min_y) // 10)
    rz = max(1, abs(max_z - min_z) // 10)
    for x in range(min_x, max_x + 1, rx):
        for y in range(min_y, max_y + 1, ry):
            for z in range(min_z, max_z + 1, ry):
                c = count_in_range(x,y,z)
                if c >= max_c and c > 0:
                    max_c = c
                    best[c].append((x,y,z))
    return max_c, best

#max_c, best = go(min_x, min_y, min_z, max_x, max_y, max_z)
#print(max_c, best[max_c])
#
#rx = max(1, abs(max_x - min_x))
#ry = max(1, abs(max_y - min_y))
#rz = max(1, abs(max_z - min_z))
#
##for next in best[max_c]:
#next = best[max_c][0]
#best_coord = [0, None]
#while rx > 0 and ry > 0 and rz > 0:
#    rx = max(1, rx) // 10
#    ry = max(1, ry) // 10
#    rz = max(1, rz) // 10
#    if rx == 0 or ry == 0 or rz == 0:
#        break
#    max_c, best = go(next[0] - rx, next[1] - ry, next[2] - rz, next[0] + rx, next[1] + ry, next[2] + rz)
#    if max_c == -1:
#        break
#    print(next, max_c, len(best[max_c]), rx, ry, rz)
#    next = best[max_c][0]
#    if max_c > best_coord[0]:
#        best_coord = (max_c, best[max_c])
#
#print(best_coord)

# (878, [(23823628, 44218566, 56748724), (23823628, 44307491, 56659799), (23823628, 44396416, 56570874), (23823628, 44485341, 56481949)])

max_c, best = 878, [(23823628, 44218566, 56748724), (23823628, 44307491, 56659799), (23823628, 44396416, 56570874), (23823628, 44485341, 56481949)]

min_x, min_y, min_z = 99999999, 99999999, 99999999
max_x, max_y, max_z = 0, 0, 0
c = 0
for n in best:
    min_x = min(min_x, n[0])
    max_x = max(max_x, n[0])
    min_y = min(min_y, n[1])
    max_y = max(max_y, n[1])
    min_z = min(min_z, n[2])
    max_z = max(max_z, n[2])

rx = max(1, abs(max_x - min_x))
ry = max(1, abs(max_y - min_y))
rz = max(1, abs(max_z - min_z))

max_c, best = go(min_x, min_y, min_z, max_x, max_y, max_z)

# (23823462, 44188931, 56778344) 898 13 1 1 1

#for next in best[max_c]:
next = best[max_c][0]
best_coord = [0, None]
while rx > 0 and ry > 0 and rz > 0:
    rx = max(1, rx // 10)
    ry = max(1, ry // 10)
    rz = max(1, rz // 10)
    if rx == 0 or ry == 0 or rz == 0:
        break
    max_c, best = go(next[0] - rx, next[1] - ry, next[2] - rz, next[0] + rx, next[1] + ry, next[2] + rz)
    if max_c == -1:
        break
    print(next, max_c, len(best[max_c]), rx, ry, rz)
    next = best[max_c][0]
    if max_c > best_coord[0]:
        best_coord = (max_c, best[max_c])

print(best_coord)