import re

initial = '####....#...######.###.#...##....#.###.#.###.......###.##..##........##..#.#.#..##.##...####.#..##.#'
initial_t = '#..#.#..##......###...###'

state = {}
for i, s in enumerate(initial):
    state[i] = True if s == '#' else False
state[len(initial)] = False
state[len(initial) + 1] = False
for i in range(-1, -20, -1):    
    state[i] = False

#print(state)

ruledefs = [
'..#.. => .',
'#.#.# => #',
'#.### => #',
'.##.. => .',
'#.#.. => #',
'.#.#. => #',
'.###. => #',
'.#### => #',
'##... => #',
'#.##. => #',
'#..## => #',
'....# => .',
'###.# => .',
'##### => #',
'..... => .',
'..#.# => .',
'.#... => #',
'##.#. => .',
'.#.## => #',
'..##. => .',
'#...# => .',
'##.## => #',
'...#. => .',
'#..#. => .',
'..### => .',
'.##.# => .',
'#.... => .',
'.#..# => #',
'####. => .',
'...## => #',
'##..# => .',
'###.. => .']

ruledefs_t = [
'...## => #',
'..#.. => #',
'.#... => #',
'.#.#. => #',
'.#.## => #',
'.##.. => #',
'.#### => #',
'#.#.# => #',
'#.### => #',
'##.#. => #',
'##.## => #',
'###.. => #',
'###.# => #',
'####. => #']

rules = []
for r in ruledefs:
    rule = {'p': True if r[2] == '#' else False,
            'res': True if r[9] == '#' else False,
            'l1': True if r[1] == '#' else False,
            'l2': True if r[0] == '#' else False,
            'r1': True if r[3] == '#' else False,
            'r2': True if r[4] == '#' else False,
            'r': r}
    rules.append(rule)

def check_r(pot, delta, key):
    potP = pot + delta
    if potP not in prev_state:
        new_pots.append(potP)
        return r[key] == False

    return prev_state[potP] == r[key]

def apply_rule(pot, r):
    if r['p'] == prev_state[pot] and check_r(pot, -1, 'l1') and check_r(pot, -2, 'l2') and check_r(pot, 1, 'r1') and check_r(pot, 2, 'r2'):
        #print(gen, 'pot', pot, 'matched', r['res'], r['r'])
        state[pot] = r['res']
    pass

def print_state(gen):
    m = min(state.keys())
    print(('0' if gen < 10 else '') + str(gen) + ': ', end='')
    for p in sorted(state.keys()):
        if p > -4:
            print('#' if state[p] else '.', end='')
    print()

print_state(0)
prev_state = dict(state)
state = {k:False for k in prev_state}
gens = 20 + 1
for gen in range(1, gens):
    new_pots = []
    for pot in state:
        for r in rules:
            apply_rule(pot, r)
    for np in new_pots:
        state[np] = False
    prev_state = dict(state)
    print_state(gen)
    state = {k:False for k in prev_state}

#print(state)
s = 0
for i, v in prev_state.items():
    if v:
        print('pot', i)
    s += (i if v else 0)
print(s)