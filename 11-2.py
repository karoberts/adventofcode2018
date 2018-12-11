import re

serial = 7857

def calc(x, y):
    rackid = x + 10
    power = (rackid * y + serial) * rackid
    power -= (power % 100)
    power = int(power / 100)
    power = power % 10
    return power - 5

def key(x,y):
    return str(x) + "," + str(y)

def caltot(x,y,s):
    return sum(grid[key(xp,yp)] for xp in range(x, x+s) for yp in range(y, y+s) )

grid = {}
for x in range(1, 301):
    for y in range(1, 301):
        grid[key(x,y)] = calc(x,y)

powgrid = {}
mx = -9999999
# answer is in size 14
# this isn't a great solution (slow), but got lucky
for s in range(14, 300):
    print(s, len(powgrid))
    if len(powgrid) > 0:
        maxkey = max(powgrid, key=lambda i:powgrid[i])
        print(s, powgrid[maxkey])
        print(s, maxkey)
    for x in range(1, 300 - s + 1):
        #print('x', x)
        for y in range(1, 300 - s + 1):
            v = caltot(x,y,s)
            if v > mx:
                mx = v
            else:
                continue
            powgrid[key(x,y) + "," + str(s)] = v

#print(powgrid)
maxkey = max(powgrid, key=lambda x:powgrid[x])
print(powgrid[maxkey])
print(maxkey)
    


