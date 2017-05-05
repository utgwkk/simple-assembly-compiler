import re


def sign_ext(d, m=8):
    if d < 0:
        d = 2 ** m + d
    return d


def parse_addr(addr):
    m = re.match(r'(\-?[0-9]+)\(([0-7])\)', addr)
    return int(m.group(2)), sign_ext(int(m.group(1)))
