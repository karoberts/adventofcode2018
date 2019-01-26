
cur = 0
twos = 0
threes = 0
with open('02.txt') as f:
    for line in f:
        ldict = {}
        for c in line.strip():
            if c in ldict:
                ldict[c] += 1
            else:
                ldict[c] = 1
            pass
        found_two = False
        found_three = False
        for c in ldict:
            if ldict[c] == 2:
                found_two = True
            if ldict[c] == 3:
                found_three = True
        if found_two:
            twos += 1
        if found_three:
            threes += 1
        pass

print('twos', twos)
print('threes', threes)
print('checksum', twos * threes)
