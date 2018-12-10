
cur = 0
freqs = set()
while True:
    with open('1-1.txt') as f:
        for line in f:
            positive = 1 if line[0] == '+' else -1
            num = int(line[1:])
            cur += (num * positive)
            if cur in freqs:
                print('dupe:', cur)
                exit()
            freqs.add(cur)
            #print('n', num, 'pos', positive, 'line', line.strip())
            pass

print('none')
