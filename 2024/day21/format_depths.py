import sys
from collections import defaultdict

depths = defaultdict(list)
for line in sys.stdin:
    line = line.strip()
    if line.startswith('depth:'):
        tokens = line.split()
        depth = tokens[1]
        end = tokens[-1]
        depths[depth].append(end)
    else:
        for d in sorted(depths):
            print(''.join(depths[d]))
        depths = defaultdict(list)
        print(line)
