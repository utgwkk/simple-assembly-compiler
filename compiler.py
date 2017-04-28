import sys
import re


def sign_ext(d, m=8):
    if d < 0:
        d = 2 ** m + d
    return d


def parse_addr(addr):
    m = re.match(r'(\-?[0-9]+)\(([0-7])\)', addr)
    return int(m.group(2)), sign_ext(int(m.group(1)))


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

    line = line.strip().lower()

    xs = line.split()

    operation = xs[0]

    operand = xs[1:]

    if operation in ARIN:
        op1 = 0b11
    elif operation in OP2:
        op1 = 0b10
        d = parse_addr(operand[1])
    elif operation == 'ld':
        op1 = 0b00
        d = parse_addr(operand[1])
    elif operation == 'st':
        op1 = 0b01
        Ra = int(operand[0])
        Rb, d = parse_addr(operand[1])
        return (op1 << 14) + (Ra << 11) + (Rb << 8) + d
    else:
        raise ValueError('Cannot parse `{}`',format(line))

def main():
    cnt = 0
    MAXCNT = 4095
    print('''WIDTH=16;
DEPTH=4096;

ADDRESS_RADIX=HEX;
DATA_RADIX=BIN;

CONTENT BEGIN''')

    for line in sys.stdin:
        line = line.strip()
        line = re.sub(r';.+$', '', line)
        if not line:
            continue
        print('  {:x}     :   {:016b}; -- {}'.format(cnt, parse_line(line), line))
        cnt += 1
    print('  [{:x}..{:x}]:0; -- MEMORY'.format(cnt, MAXCNT))
    print('END;')

if __name__ == '__main__':
    main()

