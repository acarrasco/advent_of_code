import sys

def parse(line):
    return [int(c) for c in line]

def block_iterator(description):
    empty = False
    block = 0
    file_id = 0
    for d in description:
        for _ in range(d):
            yield block, not empty and file_id
            block += 1
        if not empty:
            file_id += 1
        empty = not empty

def solve(problem):
    forward = block_iterator(problem)
    backward = reversed(list(block_iterator(problem)))
    checksum = 0
    fwd_block, fwd_file = next(forward)
    bck_block, bck_file = next(backward)

    while fwd_block <= bck_block:
        if fwd_file is not False:
            print(f'{fwd_block} * {fwd_file} = {fwd_block * fwd_file}')
            checksum += fwd_block * fwd_file
        else:
            while bck_file is False:
                bck_block, bck_file = next(backward)
            print(f'{fwd_block} * {bck_file} = {fwd_block * bck_file}')
            checksum += fwd_block * bck_file
            bck_block, bck_file = next(backward)
        fwd_block, fwd_file = next(forward)

    return checksum

print(solve(parse(sys.stdin.read().strip())))