import sys

def parse(line):
    return [int(c) for c in line]

def block_iterator(description):
    empty = False
    block_start = 0
    file_id = 0
    for size in description:
        yield block_start, not empty and file_id, size
        if not empty:
            file_id += 1
        empty = not empty
        block_start += size

def find_empty_big_enough(empty_blocks, file_block_id, file_size):
    for i, (empty_block_id, empty_size) in enumerate(empty_blocks):
        if empty_block_id > file_block_id:
            return -1
        if empty_size >= file_size:
            return i
    return -1

def defragmented_iterator(description):
    empty_blocks = [(block_id, size) for block_id, file_id, size in block_iterator(description) if file_id is False and size > 0]
    file_blocks = [(block_id, file_id, size) for block_id, file_id, size in block_iterator(description) if file_id is not False]
    while file_blocks:
        block_id, file_id, file_size = file_blocks.pop()
        empty_i = find_empty_big_enough(empty_blocks, block_id, file_size)
        if empty_i >= 0:
            empty_block_id, empty_size = empty_blocks[empty_i]
            if empty_size > file_size:
                empty_blocks[empty_i] = (empty_block_id + file_size, empty_size - file_size)
            else:
                del empty_blocks[empty_i]
            yield empty_block_id, file_id, file_size
        else:
            yield block_id, file_id, file_size

def solve(problem):
    checksum = 0
    for block_id, file_id, file_size in defragmented_iterator(problem):
        for i in range(file_size):
            checksum += (block_id + i) * file_id

    return checksum

print(solve(parse(sys.stdin.read().strip())))