import json

lines = None
with open('02-1.txt') as f:
    lines = [line.strip() for line in f]
    
for idx, line in enumerate(lines):
    for i in range(0, len(line)):
        for idx2, line2 in enumerate(lines):
            if idx2 <= idx:
                continue
            test = line2[:i] + line[i] + line2[i+1:]
            if line == test:
                print('match:', line, line2)
                print('answer', line2[:i] + line2[i+1:])


