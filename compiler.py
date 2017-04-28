import sys
import re


def parse_addr(addr):
    m = re.match(r'(\-?[0-9]+)\(([0-7])\)', addr)
    return int(m.group(2)), int(m.group(1))

def parse_line(line):
    ARIN = {
        'add': 0b0000,
        'sub': 0b0001,
        'and': 0b0010,
        'or':  0b0011,
        'xor': 0b0100,
        'cmp': 0b0101,
        'mov': 0b0110,
        'sll': 0b1000,
        'slr': 0b1001,
        'srl': 0b1010,
        'sra': 0b1011,
        'in':  0b1100,
        'out': 0b1101,
        'hlt': 0b1111,
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

    DIV = {}

    line = line.strip().lower()

    pat_1 = re.compile(r'([a-z]+)(\s+([0-7]))?(\s+([0-7]|\-?[0-9]+))?$', re.IGNORECASE)
    m1 = pat_1.match(line)

    pat_ldst = re.compile(r'([a-z]+)\s+([0-7])\s+(\-?[0-9]+\([0-7]\))$')
    m2 = pat_ldst.match(line)

    if m1:
        op = m1.group(1)
        rs = m1.group(4)
        rd = m1.group(2)

        op1 = 0

        if rd is None:
            dest = 0
        else:
            dest = int(rd)

        if rs is None:
            src = 0
        else:
            src = int(rs)

        if op == 'out':
            src, dest = dest, src

        if op in OP2:
            op3 = 0b10
            op2 = OP2[op]
            if op in BRANCH:
                dest = BRANCH[op]
            d = src
            return (op3 << 14) + (op2 << 12) + (dest << 8) + d
        elif op in ARIN:
            op3 = 0b11
            op1 = ARIN[op]
            if op in {'sll', 'slr', 'srl', 'sra'}:
                d = src
                return (op3 << 14) + (0 << 11) + (dest << 8) + (op1 << 4) + d
        else:
            raise ValueError('Invalid operation `{}`'.format(op))

        return (op3 << 14) + (src << 11) + (dest << 8) + (op1 << 4)
    elif m2:
        op = m2.group(1)
        ra = m2.group(2)
        rbd = m2.group(3)

        if op == 'ld':
            op1 = 0b00
        elif op == 'st':
            op1 = 0b01

        rai = int(ra)

        rbi, d = parse_addr(rbd)
        if d < 0:
            d = 2 ** 8 + d

        return (op1 << 14) + (rai << 11) + (rbi << 8) + d
    else:
        raise ValueError('Cannot parse `{}`'.format(line))

def main():
    cnt = 0
    MAXCNT = 4095
    print('''WIDTH=16;
DEPTH=4096;

ADDRESS_RADIX=UNS;
DATA_RADIX=BIN;

CONTENT BEGIN''')

    for line in sys.stdin:
        line = line.strip()
        line = re.sub(r';(.+)$', '', line)
        if not line:
            continue
        print('  {}     :   {:016b}; -- {}'.format(cnt, parse_line(line), line))
        cnt += 1
    print('  [{}..{}]:0000000000000000; -- MEMORY'.format(cnt, MAXCNT))
    print('END;')

if __name__ == '__main__':
    main()
