import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

# pos=<26276148,18772321,-169986>, r=84817629

def parse(fn, type, groups):

    # 17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2

    pat = re.compile(r'^(\d+) units each with (\d+) hit points(?: \(([a-z,; ]+)\))? with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)$')
    pat2 = re.compile(r'^(weak|immune) to ([a-z ,]+)$')

    t_id = {'imm': 1, 'inf': 1}
    with open(fn) as f:
        for line in (l.strip() for l in f):
            g = {}
            m = pat.match(line)
            if m is None:
                raise ArithmeticError(line)
            g['size'] = int(m.group(1))
            g['hp'] = int(m.group(2))
            g['damage'] = int(m.group(4))
            g['attack'] = m.group(5)
            g['init'] = int(m.group(6))
            g['type'] = type
            g['id'] = type + str(t_id[type])
            t_id[type] += 1
            if m.group(3):
                wis = (x.strip() for x in m.group(3).split(';'))
                for wi in wis:
                    m2 = pat2.match(wi)
                    if m2 is None:
                        raise ArithmeticError('2-' + wi)
                    g[m2.group(1)] = set(x.strip() for x in m2.group(2).split(','))
            if 'immune' not in g:
                g['immune'] = set()
            if 'weak' not in g:
                g['weak'] = set()
            groups.append(g)

def eff_power(u):
    return u['size'] * u['damage']

def sort_key(u):
    return (-eff_power(u), -u['init'])

def potential_damage(attacker, defender):
    att = attacker['attack']
    if att in defender['immune']:
        return 0
    mult = 1
    if att in defender['weak']:
        mult = 2
    return eff_power(attacker) * mult

def best_attack(attacker, groups, mapping):
    best = None
    for u in sorted(groups, key=sort_key):
        if u['id'] == attacker['id']: continue
        if u['type'] == attacker['type']: continue
        if u['id'] in mapping: continue
        pot = potential_damage(attacker, u)
        if pot > 0 and (best is None or pot > best[1]):
            best = (u, pot)
    return best

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

groups = []
parse('24-imm.txt', 'imm', groups)
parse('24-inf.txt', 'inf', groups)

# 17738

#groups = []
#parse('24-imm-test.txt', 'imm', groups)
#parse('24-inf-test.txt', 'inf', groups)

#print(json.dumps(groups, indent = 2))

while True:
    print('Immune System:')
    for g in groups:
        if g['type'] == 'imm':
            print('Group {} contains {} units'.format(g['id'], g['size']))
    print('Infection:')
    for g in groups:
        if g['type'] == 'inf':
            print('Group {} contains {} units'.format(g['id'], g['size']))

    attack_map = {}
    for unit in sorted(groups, key=sort_key):
        #print(eff_power(unit), unit)
        best = best_attack(unit, groups, attack_map)    
        if best is None:
            continue
        attack_map[best[0]['id']] = (unit, best)

    for attack in sorted(attack_map, key=lambda u:-attack_map[u][0]['init']):
        a = attack_map[attack]
        attacker = a[0]
        defender = a[1][0]
        if attacker['size'] <= 0 or defender['size'] <= 0:
            continue
        damage = potential_damage(attacker, defender)
        print('  {} attacking {} for {} damage'.format(attacker['id'], defender['id'], damage))
        killed = min(defender['size'], (damage - (damage % defender['hp'])) // defender['hp'])
        defender['size'] -= killed
        print('killed', killed, 'units')

    ngs = []
    imm_sum = 0
    inf_sum = 0
    for g in groups:
        if g['size'] == 0:
            continue
        ngs.append(g)

        if g['type'] == 'imm': imm_sum += g['size']
        if g['type'] == 'inf': inf_sum += g['size']

    groups = ngs
    if inf_sum == 0 or imm_sum == 0:
        print('imms', imm_sum, 'infs', inf_sum)
        print(json.dumps(ngs, indent=2, cls=SetEncoder))
        break

    print()

