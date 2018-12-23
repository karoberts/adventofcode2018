import re
import sys
sys.setrecursionlimit(5000)

# pos=<26276148,18772321,-169986>, r=84817629

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


min_x, min_y, min_z = 0, 0, 0
max_x, max_y, max_z = 0, 0, 0
c = 0
for b in bots:
    min_x = min(min_x, b[0] - b[4])
    max_x = max(max_x, b[0] - b[4])
    min_y = min(min_y, b[0] - b[4])
    max_y = max(max_y, b[0] - b[4])
    min_z = min(min_z, b[0] - b[4])
    max_z = max(max_z, b[0] - b[4])

print('min', min_x, min_y, min_z)
print('max', max_x, max_y, max_z)

# min/max
# -154355239 -154355239 -154355239
# 228637767 228637767 228637767


def manhat_dist(b1, b2):
    return abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])

def manhat_dist(b1, x,y,z):
    return abs(b1[0] - x) + abs(b1[1] - y) + abs(b1[2] - z)

def count_in_range(x,y,z):
    c = 0
    for b in bots:
        d = manhat_dist(b, x,y,z)
        if d <= b[3]:
            c += 1
    return c

def next_coords(lx, ly, lz, rx, ry, rz):
    nx = abs(lx - rx) // 2 + rx
    ny = abs(ly - ry) // 2 + ry
    nz = abs(lz - rz) // 2 + rz
    return nx,ny,nz

# 631  37141264 37141264 37141264

#print(count_in_range(37141264,37141264,37141264)) # 631
#print(count_in_range(38141264,38141264,38141264)) # 639
#print(count_in_range(39141264,39141264,39141264)) # 679
#print(count_in_range(39541264,39541264,39541264)) # 681
#print(count_in_range(39841264,39841264,39841264)) # 734

print(count_in_range(40141264,40141264,40141264)) # 735
print(count_in_range(40211264,40211264,40211264)) # 735
print(count_in_range(40241264,40241264,40241264)) # 735
print(count_in_range(40291264,40291264,40291264)) # 735
print(count_in_range(40341264,40341264,40341264)) # 735

#print(count_in_range(40541264,40541264,40541264)) # 734
#print(count_in_range(41141264,41141264,41141264)) # 734
#print(count_in_range(42141264,42141264,42141264)) # 733
exit()

def binary(lx, ly, lz, rx, ry, rz):
    nx, ny, nz = next_coords(lx, ly, lz, rx, ry, rz)
    in_range = count_in_range(nx, ny, nz)
    print('c', in_range, nx,ny,nz)

    nxl, nyl, nzl = next_coords(lx, ly, lz, nz, ny, nz)
    in_range = count_in_range(nxl, nyl, nzl)
    print('l', in_range, nxl,nyl,nzl)

    nxr, nyr, nzr = next_coords(nz, ny, nz, rx, ry, rz)
    in_range = count_in_range(nxr, nyr, nzr)
    print('r', in_range, nxr,nyr,nzr)

binary(max_x, max_y, max_z, min_x, min_y, min_z)