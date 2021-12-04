import sys
import itertools

inf = float('inf')


def parse_trip(line):
    cities, distance = line.split(' = ')
    place_a, place_b = cities.split(' to ')
    return (place_a, place_b, int(distance))


def build_graph(lines):
    graph = {}
    places = set()
    for line in lines:
        a, b, distance = parse_trip(line)
        graph[a, b] = distance
        graph[b, a] = distance
        places.add(a)
        places.add(b)
    return graph, places


def total_distance(graph, route):
    return sum(graph.get((a, b), inf) for a, b in zip(route, route[1:]))


graph, places = build_graph(sys.stdin.readlines())

print(max(total_distance(graph, route) for route in itertools.permutations(places)))
