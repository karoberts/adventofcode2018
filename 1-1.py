
cur = 0
with open('1-1.txt') as f:
    for line in f:
        positive = 1 if line[0] == '+' else -1
        num = int(line[1:])
        cur += (num * positive)
        #print('n', num, 'pos', positive, 'line', line.strip())
        pass

print(cur)
