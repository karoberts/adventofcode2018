import re

pat_st = re.compile(r'^(Before|After):\s+\[(\d+), (\d+), (\d+), (\d+)\]$')
pat_cmd = re.compile(r'^(\d+) (\d+) (\d+) (\d+)$')

ops = []
with open('16-1.txt') as f:
    st = 0
    cur_op = None

    for line in (l.strip() for l in f):
        if st == 0:
            m = pat_st.match(line)
            cur_op = {'b': [int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5))]}
        elif st == 1:
            m = pat_cmd.match(line)
            cur_op['c'] = [int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4))]
        elif st == 2:
            m = pat_st.match(line)
            cur_op['a'] = [int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5))]
            ops.append(cur_op)
        elif st == 3:
            pass
                
        st += 1
        st %= 4

program = []
with open('16-2.txt') as f:
    for line in (l.strip() for l in f):
        program.append([int(x) for x in line.split(' ')])

def check_outp(outp, exp_r, ra, rb):
    for i in range(0, 4):
        if i == outp:
           if ra[i] != exp_r:
               return False
        elif ra[i] != rb[i]:
            return False
    return True

def is_addr(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] + rb[i2]
    return check_outp(outp, exp_r, ra, rb)

def is_addi(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] + i2
    return check_outp(outp, exp_r, ra, rb)

def is_mulr(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] * rb[i2]
    return check_outp(outp, exp_r, ra, rb)

def is_muli(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] * i2
    return check_outp(outp, exp_r, ra, rb)

def is_banr(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] & rb[i2]
    return check_outp(outp, exp_r, ra, rb)

def is_bani(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] & i2
    return check_outp(outp, exp_r, ra, rb)

def is_borr(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] | rb[i2]
    return check_outp(outp, exp_r, ra, rb)

def is_bori(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1] | i2
    return check_outp(outp, exp_r, ra, rb)

def is_setr(rb, ra, opcode, i1, i2, outp):
    exp_r = rb[i1]
    return check_outp(outp, exp_r, ra, rb)

def is_seti(rb, ra, opcode, i1, i2, outp):
    exp_r = i1
    return check_outp(outp, exp_r, ra, rb)

def is_gtir(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if i1 > rb[i2] else 0
    return check_outp(outp, exp_r, ra, rb)

def is_gtri(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if rb[i1] > i2 else 0
    return check_outp(outp, exp_r, ra, rb)

def is_gtrr(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if rb[i1] > rb[i2] else 0
    return check_outp(outp, exp_r, ra, rb)

def is_eqir(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if i1 == rb[i2] else 0
    return check_outp(outp, exp_r, ra, rb)

def is_eqri(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if rb[i1] == i2 else 0
    return check_outp(outp, exp_r, ra, rb)

def is_eqrr(rb, ra, opcode, i1, i2, outp):
    exp_r = 1 if rb[i1] == rb[i2] else 0
    return check_outp(outp, exp_r, ra, rb)

funcs = [is_addi, is_addr, is_mulr, is_muli, is_bani, is_banr, is_bori, is_borr, is_seti, is_setr, is_gtir, is_gtri, is_gtrr, is_eqir, is_eqri, is_eqrr]
names = ['addi', 'addr', 'mulr', 'muli', 'bani', 'banr', 'bori', 'borr', 'seti', 'setr', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

mapping = {names[x]:set() for x in range(0,16)}

def check(op):
    #print(op)
    rb = op['b']
    ra = op['a']
    cmd = op['c']

    for i, f in enumerate(funcs):
        ret = f(rb, ra, cmd[0], cmd[1], cmd[2], cmd[3])
        if ret:
            mapping[names[i]].add(cmd[0])
        #print(names[i], ret)
    #print('tot', count)

for o in ops:
    check(o)

opcodes = {}

while len(opcodes) < 16:
    for f, m in mapping.items():
        #print(f, m)

        if len(m) == 1:
            opc = list(m)[0]
            opcodes[opc] = f
            for m2 in mapping.values():
                if opc in m2:
                    m2.remove(opc)

for o, m in opcodes.items():
    print(o, m)

regs = [0, 0, 0, 0]
for pline in program:
    opc = opcodes[pline[0]]
    a = pline[1]
    b = pline[2]
    c = pline[3]

    if opc == 'addr':
        regs[c] = regs[a] + regs[b]
    elif opc == 'addi':
        regs[c] = regs[a] + b
    elif opc == 'mulr':
        regs[c] = regs[a] * regs[b]
    elif opc == 'muli':
        regs[c] = regs[a] * b
    elif opc == 'banr':
        regs[c] = regs[a] & regs[b]
    elif opc == 'bani':
        regs[c] = regs[a] & b
    elif opc == 'borr':
        regs[c] = regs[a] | regs[b]
    elif opc == 'bori':
        regs[c] = regs[a] | b
    elif opc == 'setr':
        regs[c] = regs[a]
    elif opc == 'seti':
        regs[c] = a
    elif opc == 'gtir':
        regs[c] = 1 if a > regs[b] else 0
    elif opc == 'gtri':
        regs[c] = 1 if regs[a] > b else 0
    elif opc == 'gtrr':
        regs[c] = 1 if regs[a] > regs[b] else 0
    elif opc == 'eqir':
        regs[c] = 1 if a == regs[b] else 0
    elif opc == 'eqri':
        regs[c] = 1 if regs[a] == b else 0
    elif opc == 'eqrr':
        regs[c] = 1 if regs[a] == regs[b] else 0

print(regs)