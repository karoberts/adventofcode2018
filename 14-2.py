
import json
import re
import operator
from collections import Counter

from dllist import dllist

def printit():
    n = recipes.first
    while n != recipes.last:
        if n == elf1_n:
            print('[' + str(n.value) + ']', '', end='')
        elif n == elf2_n:
            print('(' + str(n.value) + ')', '', end='')
        else:
            print('', n.value, ' ', end='')
        n = n.next
    if n == elf1_n:
        print('[' + str(n.value) + ']', ' ', end='')
    elif n == elf2_n:
        print('(' + str(n.value) + ')', ' ', end='')
    else:
        print('', n.value, ' ', end='')
    print()

def printit2():
    print(x, 'elf1', elf1 + 1, 'elf2', elf2 + 1)

findit = [5,9,8,7,0,1]
#findit = [5,9,4,1,4]
#findit = [9,2,5,1,0]

elf1 = 0
elf2 = 1

recipes = dllist([3, 7])
elf1_n = recipes.nodeat(elf1)
elf2_n = recipes.nodeat(elf2)

nptr = 0
npos = 1

#while True:
for x in range(0, 100000):
    next_sum = elf1_n.value + elf2_n.value
    if next_sum < 10:
        recipes.append(next_sum)
    else:
        recipes.append(int(next_sum / 10))
        recipes.append(next_sum % 10)

    elf1_delta = 1 + elf1_n.value
    elf2_delta = 1 + elf2_n.value

    for i in range(0, elf1_delta):
        if elf1_n == recipes.last:
            elf1_n = recipes.first
            elf1 = 0
        else:
            elf1_n = elf1_n.next
            elf1 += 1
    for i in range(0, elf2_delta):
        if elf2_n == recipes.last:
            elf2_n = recipes.first
            elf2 = 0
        else:
            elf2_n = elf2_n.next
            elf2 += 1

    #printit()
    printit2()

        #print('found', n.value)
    p = recipes.last
    nptr = len(findit) - 1
    for i in range(0, len(findit)):
        if p.value != findit[nptr]:
            break
        #if nptr < 4:
        #    print(nptr)
        if nptr == 0:
            np = recipes.last
            for j in range(0, len(findit)):
                print(np.value)
                np = np.prev
            print('part2', len(recipes) - len(findit))
            exit()
        p = p.prev
        nptr -= 1

    if len(recipes) % 100000 == 0:
        print(len(recipes))
