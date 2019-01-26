import json
import re

pat = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
def parse(l):
    m = pat.match(l)
    return {'id': int(m.group(1)), 'l':int(m.group(2)), 't': int(m.group(3)), 'w':int(m.group(4)), 'h':int(m.group(5))}

lines = None
with open('03.txt') as f:
    lines = [line.strip() for line in f]

used = {}
overused = {}

for p in [parse(line) for line in lines]:
    #print(json.dumps(p))
    for x in range(p['l'], p['l'] + p['w']):
        for y in range(p['t'], p['t'] + p['h']):
            key = str(x) + ',' + str(y)
            if key in used:
                overused[key] = 1
                used[key] += 1
            else:
                used[key] = 1

for p in [parse(line) for line in lines]:
    #print(json.dumps(p))
    skip = False
    for x in range(p['l'], p['l'] + p['w']):
        for y in range(p['t'], p['t'] + p['h']):
            key = str(x) + ',' + str(y)
            if key in overused:
                skip = True
                break
        if skip:
            break
    if not skip:
        print('part2', 'id', p['id'])

#print(json.dumps(used))
"""
for k, v in used.items():
    if v > 1:
        print(k)
"""
print('part1', len(overused))
