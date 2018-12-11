import json
import re
import operator
from collections import Counter
from sortedcontainers import SortedDict
from sortedcontainers import SortedSet

def find_first():
    for n in nodes:
        if n not in rgraph:
            available.add(n)

def process_step(p):
    done.add(p)
    for n, deps in rgraph.items():
        if p in deps:
            deps.remove(p)
    
    for n in graph[p]:
        if n not in done and len(rgraph[n]) == 0:
            available.add(n)

pat = re.compile(r'^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$')
graph = {}
rgraph = {}
nodes = SortedSet()
with open('07-1.txt') as f:
    for line in f:
        m = pat.match(line.strip())
        node = m.group(1)
        dep = m.group(2)
        nodes.add(node)
        if node not in graph:
            graph[node] = SortedSet()
        graph[node].add(dep)
        if dep not in rgraph:
            rgraph[dep] = SortedSet()
        rgraph[dep].add(node)

print('nodes', nodes, 'len', len(nodes))
print('graph', graph)
print('rgraph', rgraph)

available = SortedSet()
done = set()
find_first()
print('avail', available)

first_node = available.pop(0)
print('next', first_node)
steps = [first_node]

process_step(first_node)

while len(available) > 0:
    #print('rgraph', rgraph)
    print('avail', available)

    next_node = available.pop(0)
    print('next', next_node)
    steps.append(next_node)

    if next_node not in graph:
        break
    process_step(next_node)

print(''.join(steps))

