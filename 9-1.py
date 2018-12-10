
import json
import re
import operator
from collections import Counter
from sortedcontainers import SortedDict
from sortedcontainers import SortedSet

#pat = re.compile(r'^$')

# 446 players; last marble is worth 71522 points

nplayers = 9
last_marble = 25
nplayers = 10
last_marble = 1619
nplayers = 13
last_marble = 7999

nplayers = 446
last_marble = 71522

circle = [0, 2, 1]
#marble = 2
cur_m = 1
cur_p = 3
p_scores = {n:0 for n in range(1,nplayers+1)}

for marble in range(3, last_marble + 1):

    if marble % 23 == 0:
        p_scores[cur_p] += marble
        marble_take = cur_m - 7
        if marble_take < 0:
            marble_take = len(circle) - (marble_take * -1)
        p_scores[cur_p] += circle[marble_take]
        circle = circle[:marble_take] + circle[marble_take + 1:]
        if marble_take == len(circle):
            cur_m = 0
        else:
            cur_m = marble_take
    else:
        new_pos = cur_m + 2
        if new_pos == len(circle):
            circle.append(marble)
            cur_m = new_pos
        elif new_pos > len(circle):
            circle = circle[:1] + [marble] + circle[1:]
            cur_m = 1
        else:
            circle = circle[:cur_m+2] + [marble] + circle[cur_m+2:]
            cur_m += 2

    #print(cur_p, marble, cur_m, circle)

    cur_p += 1
    if cur_p > nplayers:
        cur_p = 1

#print(cur_p, marble, cur_m, circle)
print(p_scores)
winner = max(p_scores, key=lambda x:p_scores[x])
print(p_scores[winner])