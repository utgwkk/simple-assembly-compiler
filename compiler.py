import sys
import re


def parse_register(reg):
    return int(re.sub(r'r\[([0-7])\]', r'\1', reg))

def parse_line(line):
    pat = re.compile(r'([a-z]+)(\s+(r\[[0-7]\]))?(\s+(r\[[0-7]\]|[0-9]+))?', re.IGNORECASE)
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

    DIV = {}

    line = line.strip().lower()
    m = pat.match(line)

    if m:
        op = m.group(1)
        rs = m.group(4)
        rd = m.group(2)

        op1 = 0

        if rd is None:
            dest = 0
        else:
            dest = parse_register(rd)

        if rs is None:
            src = 0
        else:
            src = parse_register(rs)

        if op == 'ld':
            op3 = 0b00
        elif op == 'st':
            op3 = 0b01
        elif op == 'li' or op in DIV:
            op3 = 0b10
        elif op in ARIN:
            op3 = 0b11
            op1 = ARIN[op]

        return (op3 << 14) + (src << 11) + (dest << 8) + (op1 << 4)
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
        print('  {}     :   {:016b}; -- {}'.format(cnt, parse_line(line), line))
        cnt += 1
    print('  [{}..{}]:0000000000000000; -- MEMORY'.format(cnt, MAXCNT))
    print('END;')

if __name__ == '__main__':
    main()
