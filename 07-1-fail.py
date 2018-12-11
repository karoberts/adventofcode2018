import json
import re
import operator
from collections import Counter
from sortedcontainers import SortedDict
from sortedcontainers import SortedSet

def clear_rgraph(node):
    for n, deps in rgraph.items():
        if node in deps:
            deps.remove(node)

def clear_graph(node):
    for n, next in graph.items():
        if node in next:
            next.remove(node)

def find_first():
    for node in active_nodes:
        if node in done:
            continue
        for rn, deps in rgraph.items():
            if len(deps) == 1 and node in deps:
                return node
    return None

def find_next():
    for node in active_nodes:
        if node in done:
            continue
        if node not in rgraph or len(rgraph[node]) == 0:
            return node;
    return None

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

steps = []
first_node = None
active_nodes = SortedSet()
for node in nodes:
    if node not in rgraph:
        print('no deps!', node)
        for rn, deps in rgraph.items():
            #if len(deps) == 1 and node in deps:
            active_nodes.add(node)

print('active', active_nodes)
done = set()
first_node = find_first()
print('first', first_node)
for n in graph[first_node]:
    active_nodes.add(n)
steps.append(first_node)
done.add(first_node)
prev_node = first_node
clear_rgraph(first_node)

while True:

    print('graph', graph)
    print('rgraph', rgraph)
    print('done', done)
    print('active', active_nodes)

    """
    possibles = SortedSet()
    for an in active_nodes:
        if an in graph:
            for n in graph[an]:
                if len(rgraph[n]) == 0:
                    possibles.add(n)

    print('new possibles', possibles)
    if len(possibles) == 0:
        break;
    """

    next_node = find_next()
    if next_node is None:
        break

    print('doing step', next_node)
    clear_graph(next_node)
    clear_rgraph(next_node)
    steps.append(next_node)
    done.add(next_node)
    if next_node not in graph:
        break
    for n in graph[next_node]:
        active_nodes.add(n)
    prev_node = next_node

print(''.join(steps))
