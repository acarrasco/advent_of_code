import sys
import json
import itertools

verbose = False

def exp_left(sn, v):
    pad = sn[-1] == '[' and '0' or ''
    for i in range(len(sn)-1, -1, -1):
        if sn[i].isdigit():
            j = i
            while sn[j].isdigit():
                j -= 1
            return sn[:j+1] + str(int(sn[j+1:i+1])+int(v)) + sn[i+1:] + pad
    return sn + '0'


def exp_right(sn, v):
    pad = sn[0] == ']' and '0' or ''
    for i in range(len(sn)):
        if sn[i].isdigit():
            j = i
            while sn[j].isdigit():
                j += 1
            return pad + sn[:i] + str(int(sn[i:j])+int(v)) + sn[j:]
    return '0' + sn


def explode(sn):
    depth = 0
    for i in range(len(sn)):
        if sn[i] == '[':
            depth += 1
        elif sn[i] == ']':
            depth -= 1
        if depth > 4:
            j = i
            while sn[j] != ',':
                j += 1
            k = j
            while sn[k] != ']':
                k += 1
            return exp_left(sn[:i], sn[i+1:j]) + exp_right(sn[k+1:], sn[j+1:k])
    return sn


def split_one(sn):
    for i in range(len(sn)):
        if sn[i:i+2].isdigit():
            v = int(sn[i:i+2])
            left = v // 2
            right = v // 2 + v % 2
            return sn[:i] + '[' + str(left) + ',' + str(right) + ']' + sn[i+2:]
    return sn


def reduce_number(sn):
    new_number = explode(sn)
    if new_number != sn:
        return reduce_number(new_number)
    new_number = split_one(sn)
    if new_number != sn:
        return reduce_number(new_number)
    return sn


def add(a, b):
    return reduce_number('[' + a + ',' + b + ']')


def mangitude(sn):
    def m(sub):
        if isinstance(sub, int):
            return sub
        else:
            left, right = sub
            return 3*m(left) + 2*m(right)
    return m(json.loads(sn))


def test(op, args, expected):
    try:
        res = op(*args)
        if res != expected:
            print('FAIL (%s%s = %s) != %s' % (op.__name__, args, res, expected))
        elif verbose:
            print('SUCCESS (%s%s == %s' % (op.__name__, args, expected))
    except:
        print('FAIL (%s(%s)' % (op.__name__, args))
        raise


test(split_one, ('[0,0]',), '[0,0]')
test(split_one, ('[15,2]',), '[[7,8],2]')
test(split_one, ('[[[[0,7],4],[15,[0,13]]],[1,1]]',), '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
test(split_one, ('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]',), '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')

test(explode,  ('[0,0]',), '[0,0]')
test(explode,  ('[[6,[5,[4,[3,2]]]],1]',), '[[6,[5,[7,0]]],3]')
test(explode,  ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',), '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
test(explode,  ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',), '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')
test(explode,  ('[[[[[9,8],1],2],3],4]',), '[[[[0,9],2],3],4]')
test(explode,  ('[7,[6,[5,[4,[3,2]]]]]',), '[7,[6,[5,[7,0]]]]')
test(explode,  ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]',), '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')
test(explode,  ('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]',), '[[[[0,7],4],[15,[0,13]]],[1,1]]')
test(explode,  ('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]',), '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

test(reduce_number,  ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]',), '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
test(reduce_number,  ('[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]',),
     '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]')

test(mangitude,  ('[[1,2],[[3,4],5]]',), 143)
test(mangitude,  ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]',), 1384)
test(mangitude,  ('[[[[1,1],[2,2]],[3,3]],[4,4]]',), 445)
test(mangitude,  ('[[[[3,0],[5,3]],[4,4]],[5,5]]',), 791)
test(mangitude,  ('[[[[5,0],[7,4]],[5,5]],[6,6]]',), 1137)
test(mangitude,  ('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',), 3488)

test(add, ('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]', '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'),
     '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]')
test(add, ('[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
           '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]'), '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]')
test(add, ('[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]',
           '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]'), '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]')
test(add, ('[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]', '[[[[4,2],2],6],[8,7]]'),
     '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')


def solve(lines):
    def sums():
        for a, b in itertools.combinations(lines, 2):
            yield add(a, b)

    return max(map(mangitude, sums()))


input = map(str.strip, sys.stdin.readlines())
print(solve(input))
