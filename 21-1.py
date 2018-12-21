import re

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

regs = [0, 0, 0, 0, 0, 0]

# part 1 = 13443200
# these regs skip a bunch of loops
regs = [13443200, 255, 19, 65536, 7782717, 256]

printregs()

ipreg = 2
stmts = 0
while True:
    if regs[ipreg] >= len(program) or regs[ipreg] < 0:
        print('HALT')
        break

    stmts += 1
    ip = regs[ipreg]
    pline = program[ip]
    printcodeline(ip, pline)
    #print('ip={} {} {}'.format(regs[ipreg], regs, pline['l']), end='')
    op = pline['op']
    a = pline['args'][0]
    b = pline['args'][1]
    c = pline['args'][2]

    if op == 'addr':
        regs[c] = regs[a] + regs[b]
    elif op == 'addi':
        regs[c] = regs[a] + b
    elif op == 'mulr':
        regs[c] = regs[a] * regs[b]
    elif op == 'muli':
        regs[c] = regs[a] * b
    elif op == 'banr':
        regs[c] = regs[a] & regs[b]
    elif op == 'bani':
        regs[c] = regs[a] & b
    elif op == 'borr':
        regs[c] = regs[a] | regs[b]
    elif op == 'bori':
        regs[c] = regs[a] | b
    elif op == 'setr':
        regs[c] = regs[a]
    elif op == 'seti':
        regs[c] = a
    elif op == 'gtir':
        regs[c] = 1 if a > regs[b] else 0
    elif op == 'gtri':
        regs[c] = 1 if regs[a] > b else 0
    elif op == 'gtrr':
        regs[c] = 1 if regs[a] > regs[b] else 0
    elif op == 'eqir':
        regs[c] = 1 if a == regs[b] else 0
    elif op == 'eqri':
        regs[c] = 1 if regs[a] == b else 0
    elif op == 'eqrr':
        regs[c] = 1 if regs[a] == regs[b] else 0

    regs[ipreg] += 1

    printregs()

print(regs)
