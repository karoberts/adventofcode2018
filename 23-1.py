import re

# pos=<26276148,18772321,-169986>, r=84817629

pat = re.compile(r'^pos=<([\-\d]+),([\-\d]+),([\-\d]+)>, r=([\d]+)$')

bots = []
i = 0
with open('23.txt') as f:
    for line in (l.strip() for l in f):
        #print(line)
        m = pat.match(line)
        bots.append([int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), i])
        i += 1


def manhat_dist(b1, b2):
    return abs(b1[0] - b2[0]) + abs(b1[1] - b2[1]) + abs(b1[2] - b2[2])

maxbot = max(bots, key=lambda x:x[3])

print(maxbot)

c = 0
for b in bots:
    #if b[4] == maxbot[4]:
        #continue
    if maxbot[3] >= manhat_dist(maxbot, b):
        c += 1

print(c)