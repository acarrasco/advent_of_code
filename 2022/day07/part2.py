import sys
import collections

TOTAL_SIZE = 70000000
MIN_SIZE = 30000000

def parse(lines):
    names_stack = []
    dir_sizes = collections.defaultdict(int)
    for line in lines:
        if line.startswith('$'):
            _, command, *args = line.split()
            if command == 'cd':
                new_dir, = args
                if new_dir == '..':
                    names_stack.pop()
                else:
                    names_stack.append(new_dir)
        else:
            x, n = line.split()
            if x != 'dir':
                size = int(x)
                dirname = ''
                for d in names_stack:
                    dirname += d + '/'
                    dir_sizes[dirname] += size
            
    return dir_sizes

def solve(dir_sizes):
    used = dir_sizes['//']
    need_to_free = used + MIN_SIZE - TOTAL_SIZE
    return min(x for x in dir_sizes.values() if x >= need_to_free)

print(solve(parse(sys.stdin)))