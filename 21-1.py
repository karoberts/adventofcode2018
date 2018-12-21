import re

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

regs = [0, 0, 0, 0, 0, 0]

zero = 65000

ipreg = 2
stmts = 0
while True:
    if regs[ipreg] >= len(program) or regs[ipreg] < 0:
        print('HALT')
        break

    if stmts > 100:
        zero += 1
        if zero % 1000 == 0:
            print('trying', zero)
        regs = [zero, 0, 0, 0, 0, 0,]
        stmts = 0

    stmts += 1
    ip = regs[ipreg]
    pline = program[ip]
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

    #print(regs)

    regs[ipreg] += 1

print(regs)
