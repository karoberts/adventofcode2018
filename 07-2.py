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

    if p not in graph:
        return
    
    for n in graph[p]:
        if n not in done and len(rgraph[n]) == 0:
            available.add(n)

def get_worker():
    for i, w in enumerate(workers):
        if w is None:
            return i
    return None

def check_done_workers():
    nodes_done = []
    for i, w in enumerate(workers):
        if w is not None and w[1] == time:
            print('worker done', w)
            nodes_done.append(w)
            workers[i] = None
    return nodes_done
            
def get_time(n):
    return ord(n) - ord('A') + delay

pat = re.compile(r'^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$')
graph = {}
rgraph = {}
nodes = SortedSet()

nworkers = 5
delay = 60 
workers = nworkers * [None]

with open('07.txt') as f:
    for line in f:
        m = pat.match(line.strip())
        node = m.group(1)
        dep = m.group(2)
        nodes.add(node)
        nodes.add(dep)
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
steps = []
time = 0
find_first()
print('avail', available)

first_node = available.pop(0)
w = get_worker()
print('assign', w, first_node, time + get_time(first_node))
workers[w] = (first_node, time + get_time(first_node))

print('next', first_node, 'w', workers)

while len(done) < len(nodes):

    while len(available) > 0:
        w = get_worker()
        if w is not None:
            next_node = available.pop(0)
            print('assign', w, next_node, time + get_time(next_node))
            workers[w] = (next_node, time + get_time(next_node))
        else:
            break

    dw = check_done_workers()

    if len(dw) > 0:
        for d in dw:
            steps.append(d[0])
            process_step(d[0])

    time += 1
    print('time now', time)

print (''.join(steps))
