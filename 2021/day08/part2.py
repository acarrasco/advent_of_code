import sys

digit_to_segments = dict(enumerate(map(set, [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg', ])))


def make_segment_sets(digits):
    return [set(s) for s in digits]


def parse_line(line):
    all_digits, output = line.strip().split(' | ')
    return make_segment_sets(all_digits.split()), make_segment_sets(output.split())


def only_match(predicate, seq):
    try:
        match, = filter(predicate, seq)
        return match
    except:
        print(list(filter(predicate, seq)))
        raise


def test(v, result):
    if isinstance(v, int):
        assert digit_to_segments[v] == result, (v, digit_to_segments[v], result)
    else:
        assert v == result


def manual_remap(all_scrambled_digits, test=lambda x, y: None):
    one_segments = only_match(lambda x: len(x) == 2, all_scrambled_digits)
    test(1, one_segments)

    four_segments = only_match(lambda x: len(x) == 4, all_scrambled_digits)
    test(4, four_segments)

    seven_segments = only_match(lambda x: len(x) == 3, all_scrambled_digits)
    test(7, seven_segments)

    eight_segments = only_match(lambda x: len(x) == 7, all_scrambled_digits)
    test(8, eight_segments)

    a_segment = seven_segments - one_segments
    test({'a'}, a_segment)

    six_segments = only_match(lambda x: len(x) == 6 and 1 == len(one_segments & x), all_scrambled_digits)
    test(6, six_segments)

    c_segment = eight_segments - six_segments
    test({'c'}, c_segment)

    f_segment = one_segments - c_segment
    test({'f'}, f_segment)

    e_g_segments = six_segments - four_segments - a_segment
    test({'e', 'g'}, e_g_segments)

    nine_segments = only_match(lambda x: len(x) == 6 and len(x & e_g_segments) == 1, all_scrambled_digits)
    test(9, nine_segments)

    e_segment = eight_segments - nine_segments
    test({'e'}, e_segment)

    zero_segments = only_match(lambda x: len(x) == 6 and x != six_segments and x != nine_segments, all_scrambled_digits)
    test(0, zero_segments)

    d_segment = eight_segments - zero_segments
    test({'d'}, d_segment)

    b_segment = four_segments - (d_segment | one_segments)
    test({'b'}, b_segment)

    g_segment = e_g_segments - e_segment
    test({'g'}, g_segment)

    two_segments = eight_segments - b_segment - f_segment
    test(2, two_segments)

    three_segments = eight_segments - b_segment - e_segment
    test(3, three_segments)

    five_segments = six_segments - e_segment
    test(5, five_segments)

    return {
        # 'a': a_segment,
        # 'b': b_segment,
        # 'c': c_segment,
        # 'd': d_segment,
        # 'e': e_segment,
        # 'f': f_segment,
        # 'g': g_segment,
        '0': zero_segments,
        '1': one_segments,
        '2': two_segments,
        '3': three_segments,
        '4': four_segments,
        '6': six_segments,
        '5': five_segments,
        '7': seven_segments,
        '8': eight_segments,
        '9': nine_segments
    }


def find_digit(remapped_segments, scrambled):
    for i, v in remapped_segments.items():
        if v == scrambled:
            return i


def decode_output(case):
    all_digits, output = case
    remapped = manual_remap(all_digits)
    return int(''.join(find_digit(remapped, scrambled) for scrambled in output))


input = map(parse_line, sys.stdin.readlines())
# print(manual_remap(digit_to_segments.values(), test))
print(sum(decode_output(case) for case in input))
