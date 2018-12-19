import re

pat_cmd = re.compile(r'^([a-z]+) (\d+) (\d+) (\d+)$')

program = []
with open('19.txt') as f:
    st = 0
    cur_op = None

    #program.append({'op': 'seti', 'args': [1, 0, 0], 'l': 'seti 1 0 0'})

    for line in (l.strip() for l in f):
        if line.startswith('#'):
            continue

        m = pat_cmd.match(line)
        program.append({'op': m.group(1), 'args': [int(m.group(2)),int(m.group(3)),int(m.group(4))], 'l': line})

regs = [0, 0, 0, 0, 0, 0]

# part 2
regs[0] = 1
# 10551367 = 2801 × 3767

ipreg = 3
stmts = 0
while True:
    if regs[ipreg] >= len(program) or regs[ipreg] < 0:
        print('HALT')
        break

    stmts += 1
    ip = regs[ipreg]
    pline = program[ip]
    if stmts % 100000 == 0:
        print(stmts)
    #print('ip', ip)
    if ip == 7 or stmts % 100000 == 0:
     #   print(regs[4])
        print('ip={} {} {}'.format(regs[ipreg], regs, pline['l']), end='')
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

    if ip == 7 or stmts % 100000 == 0:
        print(regs)

    if regs[ipreg] == 2 and regs == [0, 1, 0, 2, 1000, 10551367]:
        print('found1', stmts)
        regs[4] = 10551366

    if stmts > 8013 and regs[ipreg] == 2 and regs == [1, 2, 0, 2, 38993, 10551367]:
        print('found2', stmts)
        regs[4] = 10551366

    if stmts > 38993 and regs[ipreg] == 2 and regs == [1, 3, 0, 2, 4469, 10551367]:
        print('found3', stmts)
        regs[4] = 2801
        regs[1] = 3766

    regs[ipreg] += 1

print(regs)
