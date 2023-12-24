import sys
import re

exps = [f'(r{c}) = ([0-9]+)' for c in 'xyz']

res = {}
for line in sys.stdin:
    for ex in exps:
        m = re.findall(ex, line)
        if m:
            (c, v), = m
            res[c] = int(v)

print(sum(res.values()))