import json
import re
import operator
from collections import Counter

pat = re.compile(r'^\[\d{4}-(\d{2}-\d{2}) (\d{2}):(\d{2})\] (wakes up|falls asleep|Guard #\d+ begins shift)$')
pat2 = re.compile(r'^Guard #(\d+) begins shift$')
def parse(l):
    m = pat.match(l)
    m2 = pat2.match(m.group(4))

    return {'sk': m.group(1) + m.group(2) + m.group(3), 'day': m.group(1), 'h': int(m.group(2)), 'm': int(m.group(3)), 'g': int(m2.group(1)) if m2 is not None else None, 'ev':m.group(4) if m2 is None else 'shift'}

def get_times(e1, e2):
    return [m for m in range(e1['m'], e2['m'])]

entries = None
with open('04.txt') as f:
    entries = sorted([parse(line.strip()) for line in f], key=lambda x:x['sk'])

curday = None
curguard = -1
sleeping = None
sleeps = {}
totsleeps = {}
for e in entries:
    #print(e['day'], e['h'], e['m'], e['g'], e['ev'])

    if e['day'] != curday:
        curday = e['day']
        #print('starting day', curday)

    if e['ev'] == 'shift' and e['g'] != curguard:
        curguard = e['g']
        if curguard not in sleeps:
            sleeps[curguard] = []
            totsleeps[curguard] = 0
        #print('guard start', curguard)
        continue

    if e['ev'] == 'falls asleep':
        #print(curguard, 'sleep', e['h'], e['m'])
        sleeping = e
        pass

    if e['ev'] == 'wakes up':
        #print(curguard, 'wake', e['h'], e['m'])
        minutes = get_times(sleeping, e)
        #print(json.dumps(minutes))
        totsleeps[curguard] = totsleeps[curguard] + len(minutes)
        sleeps[curguard].extend(minutes)
        sleeping = None
        pass

max_g = 0
max_m = 0
max_c = 0
for g in sleeps:
    if len(sleeps[g]) == 0:
        continue
    c = Counter(sleeps[g])
    #print(c)
    maxmin = max(c, key=lambda x:c[x])
    print(g, maxmin, c[maxmin])
    if c[maxmin] > max_c:
        max_c = c[maxmin]
        max_g = g
        max_m = maxmin

print(max_g, max_m, max_c)
print(max_g * max_m)

#maxsleeper = max(totsleeps, key=lambda k: totsleeps[k])
#print (maxsleeper)
#print(sleeps[maxsleeper])
#minutes = Counter(sleeps[maxsleeper])
#maxmin = max(minutes, key=lambda x:minutes[x])
#print (maxmin * maxsleeper)
