
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

elvesguess = 598701
#elvesguess = 2018

elf1 = 0
elf2 = 1

recipes = dllist([3, 7])
elf1_n = recipes.nodeat(elf1)
elf2_n = recipes.nodeat(elf2)

while len(recipes) < elvesguess + 10:
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
        else:
            elf1_n = elf1_n.next
    for i in range(0, elf2_delta):
        if elf2_n == recipes.last:
            elf2_n = recipes.first
        else:
            elf2_n = elf2_n.next

    #printit()

n = recipes.first
for i in range(0, elvesguess):
    #print(n.value, '', end='')
    n = n.next
#print(' | ', end='')
findit = []
print('part1 ', end='')
for i in range(0, 10):
    print(n.value, end='')
    n = n.next
print()