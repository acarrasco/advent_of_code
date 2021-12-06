import sys
import re
import numpy

exp = '([a-zA-Z]+): capacity (-?[0-9]), durability (-?[0-9]), flavor (-?[0-9]), texture (-?[0-9]), calories ([0-9])'


def parse_ingredient(line):
    groups = re.match(exp, line).groups()
    name, *properties = groups
    return list(map(int, properties))


def calculate_score(ingredients_matrix, amounts):
    agg = amounts * ingredients_matrix
    agg[agg < 0] = 0
    if agg[0,-1] != 500:
        return 0
    return agg[:, :-1].prod()


def parse_input(lines):
    ingredients = [parse_ingredient(line) for line in lines]
    return numpy.matrix(ingredients)


def ingredients_permutations(n, total, current):
    if n == 1:
        yield current + [total]
    else:
        for i in range(total + 1):
            for rest in ingredients_permutations(n-1, total-i, [i] + current):
                yield rest


ingredients = parse_input(sys.stdin.readlines())
print(max(calculate_score(ingredients, numpy.matrix(perm))
          for perm in ingredients_permutations(len(ingredients), 100, [])))
