import sys
import collections

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
    return sum(x for x in dir_sizes.values() if x < 100000)

print(solve(parse(sys.stdin)))