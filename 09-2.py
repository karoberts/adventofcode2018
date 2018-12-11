
import json
import re
import operator
from collections import Counter
from sortedcontainers import SortedDict
from sortedcontainers import SortedSet

from dllist import dllist

#pat = re.compile(r'^$')

# 446 players; last marble is worth 71522 points

nplayers = 9
last_marble = 25
nplayers = 10
last_marble = 1619
nplayers = 13
last_marble = 7999
nplayers = 17
last_marble = 1104
nplayers = 21
last_marble = 6111
nplayers = 30
last_marble = 5807

nplayers = 446
last_marble = 7152200

circle = dllist([0, 2, 1])
#marble = 2
cur_m = 1
cur_mn = circle.nodeat(cur_m)
cur_p = 3
p_scores = {n:0 for n in range(1,nplayers+1)}

for marble in range(3, last_marble + 1):

    if marble % 10000 == 0:
        print('m', marble, marble / last_marble * 100.0)

    if marble % 23 == 0:
        p_scores[cur_p] += marble
        marble_take = cur_m - 7
        mt_node = None
        if marble_take < 0:
            nmove = marble_take * -1
            marble_take = len(circle) - nmove
            mt_node = circle.last
            for i in range(0, nmove - 1):
                mt_node = mt_node.prev
        else:
            mt_node = cur_mn
            for i in range(0, 7):
                mt_node = mt_node.prev

        p_scores[cur_p] += mt_node.value #circle[marble_take]
        #circle = circle[:marble_take] + circle[marble_take + 1:]
        if marble_take == len(circle):
            cur_m = 0
            cur_mn = circle.first
        else:
            cur_m = marble_take
            cur_mn = mt_node.next
        circle.remove(mt_node)
    else:
        new_pos = cur_m + 2
        if new_pos == len(circle):
            cur_mn = circle.appendright(marble)
            cur_m = new_pos
        elif new_pos > len(circle):
            #circle = circle[:1] + [marble] + circle[1:]
            cur_mn = circle.insert(marble, None, circle.first)
            cur_m = 1
        else:
            #circle = circle[:cur_m+2] + [marble] + circle[cur_m+2:]
            cur_mn = circle.insert(marble, None, cur_mn.next)
            cur_m += 2

    #print(cur_p, marble, cur_m, circle)

    cur_p += 1
    if cur_p > nplayers:
        cur_p = 1

#print(cur_p, marble, cur_m, circle)
print(p_scores)
winner = max(p_scores, key=lambda x:p_scores[x])
print(p_scores[winner])


