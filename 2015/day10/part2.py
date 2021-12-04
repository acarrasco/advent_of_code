import itertools


def look_and_say(input):
    return ''.join('%s%s' % (len(list(it)), n) for n, it in itertools.groupby(input))


def repeat(f, input, times):
    if times == 0:
        return input
    else:
        return repeat(f, f(input), times - 1)

def test(s, expected):
    res = look_and_say(s)
    if res != expected:
        raise Exception('Wrong result', s, expected, res)


test('1', '11')
test('11', '21')
test('21', '1211')
print(len(repeat(look_and_say, '1321131112', 50)))
