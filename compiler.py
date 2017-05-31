import sys
import utils
import re
from intermediate import *


def parse_line(line):
    ARIN = {
        'add': 0b0000,
        'sub': 0b0001,
        'and': 0b0010,
        'or':  0b0011,
        'xor': 0b0100,
        'cmp': 0b0101,
        'mov': 0b0110,
        'adi': 0b0111,
        'sll': 0b1000,
        'slr': 0b1001,
        'srl': 0b1010,
        'sra': 0b1011,
        'in':  0b1100,
        'out': 0b1101,
        'hlt': 0b1111,
    }

    SHIFTS = {
        'sll', 'slr', 'srl', 'sra', 'adi'
    }

    OP2 = {
        'li': 0b000,
        'b': 0b100,
        'be': 0b111,
        'blt': 0b111,
        'ble': 0b111,
        'bne': 0b111,
    }

    BRANCH = {
        'be': 0b000,
        'blt': 0b001,
        'ble': 0b010,
        'bne': 0b011,
    }

    line = line.strip().lower()

    if line.endswith(':'):
        labelname = line[:-1]
        return Label(labelname)

    xs = line.split()

    operation = xs[0]

    operand = xs[1:]

    if operation in ARIN:
        op1 = 0b11
        op3 = ARIN[operation]
        if operation in SHIFTS:
            Rd = int(operand[0])
            if operation == 'adi':
                d = utils.sign_ext(int(operand[1]), 4)
            else:
                d = int(operand[1])
            return Operation(op1, 0, Rd, (op3 << 4) + d)
        elif operation == 'in':
            Rd = int(operand[0])
            return Operation(op1, 0, Rd, op3 << 4)
        elif operation == 'out':
            Rs = int(operand[0])
            return Operation(op1, Rs, 0, op3 << 4)
        elif operation == 'hlt':
            return Operation(op1, 0, 0, op3 << 4)
        else:
            Rd = int(operand[0])
            Rs = int(operand[1])
            return Operation(op1, Rs, Rd, op3 << 4)
    elif operation in OP2:
        op1 = 0b10
        op2 = OP2[operation]
        if operation in BRANCH:
            if operand[0][-1].isdigit():
                d = RelativeLine(int(operand[0]))
            else:
                d = Label(operand[0])
            return Operation(op1, op2, BRANCH[operation], d)
        else:
            Rb = int(operand[0])
            if operation == 'li':
                d = utils.sign_ext(int(operand[1]))
            elif operand[1][-1].isdigit():
                d = RelativeLine(int(operand[1]))
            else:
                d = Label(operand[1])
            return Operation(op1, op2, Rb, d)
    elif operation == 'ld':
        op1 = 0b00
        Rb = int(operand[0])
        Ra, d = utils.parse_addr(operand[1])
        return Operation(op1, Ra, Rb, d)
    elif operation == 'st':
        op1 = 0b01
        Rb = int(operand[0])
        Ra, d = utils.parse_addr(operand[1])
        return Operation(op1, Ra, Rb, d)
    else:
        raise ValueError('Cannot parse `{}`',format(line))

def main():
    cnt = 0
    MAXCNT = 4095

    program = []
    labels = dict()

    for line in sys.stdin:
        line = re.sub(r';.*', '', line)
        line = line.strip()
        if not line:
            continue

        result = parse_line(line)

        if isinstance(result, Operation):
            program.append(result)
            cnt += 1
        elif isinstance(result, Label):
            labels[result.name] = cnt
        else:
            raise ValueError('yabai at cnt {}'.format(cnt))

    # Resolve labels
    for idx, code in enumerate(program):
        if isinstance(code.d, Label):
            if code.d.name in labels:
                dist = utils.sign_ext(utils.distance(idx, labels[code.d.name]) - 1)
                print('{} -> {} : {}'.format(idx, code.d.name, dist), file=sys.stderr)
                program[idx].d = dist
            else:
                raise KeyError('Label `{}` does not exist'.format(code.d.name))
    
    dump(program)


def dump(program):
    print('''WIDTH=16;
DEPTH=4096;

ADDRESS_RADIX=BIN;
DATA_RADIX=BIN;

CONTENT BEGIN''')
    for cnt, line in enumerate(program):
        print('  {0:016b}     :   {1:016b};'.format(cnt, int(line)))
    print('END;')


if __name__ == '__main__':
    main()
