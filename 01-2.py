
cur = 0
freqs = set()
with open('01.txt') as f:
    nums = [int(line[1:]) * (1 if line[0] == '+' else -1) for line in f.readlines()]

while True:
    for num in nums:
        cur += num
        if cur in freqs:
            print('dupe:', cur)
            exit()
        freqs.add(cur)
        #print('n', num, 'pos', positive, 'line', line.strip())
        pass

print('none')
