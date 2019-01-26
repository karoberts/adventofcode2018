import re

serial = 7857

def calc(x, y):
    rackid = x + 10
    power = (rackid * y + serial) * rackid
    power -= (power % 100)
    power = int(power / 100)
    power = power % 10
    return power - 5

def caltot(x,y):
    return sum(grid[(xp,yp)] for xp in range(x, x+3) for yp in range(y, y+3) )

grid = {}
for x in range(1, 301):
    for y in range(1, 301):
        grid[(x,y)] = calc(x,y)

powgrid = {}
for x in range(1, 298):
    for y in range(1, 298):
        powgrid[(x,y)] = caltot(x,y)

#print(powgrid)
maxkey = max(powgrid, key=lambda x:powgrid[x])
print(powgrid[maxkey])
print(maxkey)
    
