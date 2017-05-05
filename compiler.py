import sys
import utils
from intermediate import *


def parse_line(line, labels=None):
    if labels is None:
        labels = dict()

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
        return UnknownLabel(labelname)

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
            d = utils.sign_ext(int(operand[0]))
            return Operation(op1, op2, 0, (BRANCH[operation] << 8) + d)
        else:
            Rb = int(operand[0])
            d = utils.sign_ext(int(operand[1]))
            return Operation(op1, op2, Rb, d)
    elif operation == 'ld':
        op1 = 0b00
        Ra = int(operand[0])
        Rb, d = utils.parse_addr(operand[1])
        return Operation(op1, Ra, Rb, d)
    elif operation == 'st':
        op1 = 0b01
        Ra = int(operand[0])
        Rb, d = utils.parse_addr(operand[1])
        return Operation(op1, Ra, Rb, d)
    else:
        raise ValueError('Cannot parse `{}`',format(line))

def main():
    cnt = 0
    MAXCNT = 4095
    print('''WIDTH=16;
DEPTH=4096;

ADDRESS_RADIX=HEX;
DATA_RADIX=DEC;

CONTENT BEGIN''')

    for line in sys.stdin:
        line = line.strip()
        line = re.sub(r';.+$', '', line)
        if not line:
            continue
        print('  {:x}     :   {:d}; -- {}'.format(cnt, parse_line(line), line))
        cnt += 1
    print('  [{:x}..{:x}]:0; -- MEMORY'.format(cnt, MAXCNT))
    print('END;')

if __name__ == '__main__':
    main()
