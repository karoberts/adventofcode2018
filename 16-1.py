import re

pat_st = re.compile(r'^(Before|After):\s+\[(\d+), (\d+), (\d+), (\d+)\]$')
pat_cmd = re.compile(r'^(\d+) (\d+) (\d+) (\d+)$')

ops = []
with open('16-1.txt') as f:
#if 1 == 1:
    st = 0
    cur_op = None

#    f = ['Before: [3, 2, 1, 1]', '9 2 1 2', 'After:  [3, 2, 2, 1]']

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

def check(op):
    #print(op)
    rb = op['b']
    ra = op['a']
    cmd = op['c']

    count = 0
    for i, f in enumerate(funcs):
        ret = f(rb, ra, cmd[0], cmd[1], cmd[2], cmd[3])
        count += (1 if ret else 0)
        #print(names[i], ret)
    #print('tot', count)
    return count

count = 0
for o in ops:
    if check(o) >= 3:
        count += 1
print(count)
