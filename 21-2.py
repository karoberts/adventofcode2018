import re

# from reddit, mine worked originally and I somehow got the answer, but it doesn't seem runnable anymore
seen = set()
CS = set()
final = None

C = 10283511
D = 65536
while True:
    E = D % 256
    C += E
    C = (C%(2**24) * 65899) % (2**24)
    if D < 256:
        if C not in CS:
            final = C
        CS.add(C)
        D = C | (2**16)
        if D in seen:
            print(final)
            break
        seen.add(D)
        C = 10283511
        continue

    D = D//256
exit()

def printcodeline(ip, pline):
    def print_r_op(a,b,c,op):
        if c == 2:
            print('IP: ', end='')
        elif a == 0 or c == 0 or b == 0:
            print('R0: ', end='')
        if a == c:
            print('r{} {}= r{}'.format(c, op, b))
        elif b == c:
            print('r{} {}= r{}'.format(c, op, a))
        else:
            print('r{} = r{} {} r{}'.format(c, a, op, b))

    def print_i_op(a,b,c,op):
        if c == 2:
            print('IP: ', end='')
        elif a == 0 or c == 0:
            print('R0: ', end='')
        if a == c:
            print('r{} {}= {}'.format(c, op, b))
        else:
            print('r{} = r{} {} {}'.format(c, a, op, b))

    def print_cmp(a,b,c,op):
        if c == 2:
            print('IP: ', end='')
        elif a == 'r0' or c == 0 or b == 'r0':
            print('R0: ', end='')
        print('r{} = 1 if {} {} {} else 0'.format(c, a, op, b))

    op = pline['op']
    a = pline['args'][0]
    b = pline['args'][1]
    c = pline['args'][2]

    print('{}: '.format(ip), end='')

    if op == 'addr':
        print_r_op(a,b,c,'+')
    elif op == 'addi':
        print_i_op(a, b, c, '+')
    elif op == 'mulr':
        print_r_op(a,b,c,'*')
    elif op == 'muli':
        print_i_op(a, b, c, '*')
    elif op == 'banr':
        print_r_op(a,b,c,'&')
    elif op == 'bani':
        print_i_op(a, '0x{:02X}'.format(b), c, '&')
    elif op == 'borr':
        print_r_op(a,b,c,'|')
    elif op == 'bori':
        print_i_op(a, '0x{:02X}'.format(b), c, '|')
    elif op == 'setr':
        if c == 2:
            print('IP: ', end='')
        elif a == 0 or c == 0:
            print('R0: ', end='')
        print('r{} = r{}'.format(c,a))
    elif op == 'seti':
        if c == 2:
            print('IP: ', end='')
        elif c == 0:
            print('R0: ', end='')
        print('r{} = {}'.format(c,a))
    elif op == 'gtir':
        print_cmp(a, 'r'+str(b), c, '>')
    elif op == 'gtri':
        print_cmp('r'+str(a), b, c, '>')
    elif op == 'gtrr':
        print_cmp('r'+str(a), 'r'+str(b), c, '>')
    elif op == 'eqir':
        print_cmp(a, 'r'+str(b), c, '==')
    elif op == 'eqri':
        print_cmp('r'+str(a), b, c, '==')
    elif op == 'eqrr':
        print_cmp('r'+str(a), 'r'+str(b), c, '==')

def printcode():
    for i, pline in enumerate(program):
        printcodeline(i, pline)

def printregs():
    print('[', end='')
    for i, v in enumerate(regs):
        print('r{}: {}, '.format(i, v), end='')
    print(']')

pat_cmd = re.compile(r'^([a-z]+) (\d+) (\d+) (\d+)$')

program = []
with open('21.txt') as f:
    st = 0
    cur_op = None

    #program.append({'op': 'seti', 'args': [1, 0, 0], 'l': 'seti 1 0 0'})

    for line in (l.strip() for l in f):
        if line.startswith('#'):
            continue

        m = pat_cmd.match(line)
        program.append({'op': m.group(1), 'args': [int(m.group(2)),int(m.group(3)),int(m.group(4))], 'l': line})

#printcode();
#exit()

# < 7782717

# 10_283_511 7782717
# 10551679
# 13377301


# part 2
i = 10283511
items = set()
#items.add(i)
last = 0
# while True:
#     n = (i * 65899) & 0xFFFFFF
#     #n = (n * 65899) & 0xFFFFFF
#     if len(items) > 2097148:
#         print(i, n)
#     if n in items:
#         print('part2', last, len(items))
#         break
#     items.add(n)
#     i = n
#     last = n
#     if len(items) % 100000 == 0:
#         print(i, len(items), len(items) / (256*256*256.0 * .01))
#     break
#print(items)
#print(len(items))
#exit()

regs = [0, 0, 0, 0, 0, 0]

# part 1 = 13443200
# these regs skip a bunch of loops
regs = [0, 255, 19, 65536, 7782717, 256]
regs = [839719, 255, 19, 65536, 14776799, 256]

# 10349410

# 6601554 answer->7717135

printregs()

fs = {}
fs['addr'] = lambda a,b: regs[a] + regs[b]
fs['addi'] = lambda a,b: regs[a] + b
fs['mulr'] = lambda a,b: regs[a] * regs[b]
fs['muli'] = lambda a,b: regs[a] * b
fs['banr'] = lambda a,b: regs[a] & regs[b]
fs['bani'] = lambda a,b: regs[a] & b
fs['borr'] = lambda a,b: regs[a] | regs[b]
fs['bori'] = lambda a,b: regs[a] | b
fs['setr'] = lambda a,b: regs[a]
fs['seti'] = lambda a,b: a
fs['gtir'] = lambda a,b: 1 if a > regs[b] else 0
fs['gtri'] = lambda a,b: 1 if regs[a] > b else 0
fs['gtrr'] = lambda a,b: 1 if regs[a] > regs[b] else 0
fs['eqir'] = lambda a,b: 1 if a == regs[b] else 0
fs['eqri'] = lambda a,b: 1 if regs[a] == b else 0
fs['eqrr'] = lambda a,b: 1 if regs[a] == regs[b] else 0

ipreg = 2
stmts = 0
while True:
    if regs[ipreg] >= len(program) or regs[ipreg] < 0:
        print('HALT')
        break

    stmts += 1
    ip = regs[ipreg]
    pline = program[ip]
    #printcodeline(ip, pline)
    #print('ip={} {} {}'.format(regs[ipreg], regs, pline['l']), end='')
    op = pline['op']
    a = pline['args'][0]
    b = pline['args'][1]
    c = pline['args'][2]

    f = fs[op]
    regs[c] = f(a,b)

    regs[ipreg] += 1

    if regs[ipreg] == 29:
        if regs[4] in items:
            print(regs[4], last)
            exit()
        items.add(regs[4])
        #printregs()
        #print(len(items) / 0xffffff * 100.0)
        last = regs[4]
    #printregs()

print(regs)
