import sys

from pprint import pprint

weights = sorted(map(int, sys.stdin), reverse=True)
total = sum(weights)

target = total // 4

def prod(seq):
    p = 1
    for n in seq:
        p *= n
    return p

def find_groups_of_weight(candidates, remaining_weights, remaining_sum, target):    
    if target == 0:
        yield candidates
    elif remaining_sum < target:
        return
    else:
        for i, w in enumerate(remaining_weights):
            remaining_sum -= w
            if w <= target:
                next_candidates = candidates + (w,)
                next_remaining_weights = remaining_weights[i+1:]
                next_target = target - w
                yield from find_groups_of_weight(next_candidates,
                                                 next_remaining_weights,
                                                 remaining_sum,
                                                 next_target)

group_candidates = find_groups_of_weight((), weights, total, target)
ranked_candidates = sorted(group_candidates, key=lambda g: (len(g), prod(g)))

for g in ranked_candidates:
    remaining_weights = sorted(set(weights) - set(g), reverse=True)
    trunk_groups = find_groups_of_weight((), remaining_weights, target*3, target)
    for tg in trunk_groups:
        remaining_weights_sides = sorted(set(remaining_weights) - set(tg), reverse=True)
        side_groups = find_groups_of_weight((), remaining_weights_sides, target*2, target)
        if any(side_groups):
            print(prod(g))
            sys.exit()