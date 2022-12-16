import sys
import re
from math import inf
from collections import defaultdict

LINE_EXP = 'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z]+(?:, [A-Z]+)*)'

def parse_line(line):
    m = re.match(LINE_EXP, line)
    if not m:
        print(line)
    valve, flow_rate, tunnels = m.groups()
    return valve, int(flow_rate), tuple(t.strip() for t in tunnels.split(','))

def parse(lines):
    graph = {}
    flows = {}
    for valve, flow, tunnels in map(parse_line, lines):
        graph[valve] = tunnels
        flows[valve] = flow
    return graph, flows

def calculate_distances(graph):
    distances = {}
    for i in graph:
        distances[i, i] = 0
        for j in graph[i]:
            distances[i,j] = 1
    for i in graph:
        for j in graph:
            for k in graph:
                if distances.get((i, k), inf) + distances.get((k, j), inf) < distances.get((i, j), inf):
                    distances[i, j] = distances[i, k] + distances[k, j]
    return distances

def prune_stuck_valves(distances, flows):
    return {
        (i, j) : distance for (i, j), distance in distances.items()
        if i != j and (i == 'AA' or flows[i] != 0) and flows[j] != 0
    }

def b_star(start, neighbors, d, h):
    open_set = {start}

    g_score = defaultdict(lambda: 0)
    g_score[start] = 0

    f_score = defaultdict(lambda: 0)
    f_score[start] = h(start)

    while open_set:
        current = max(open_set, key=f_score.__getitem__)
        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = d(neighbor)
            if tentative_g_score > g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                fs = tentative_g_score + h(neighbor)
                f_score[neighbor] = fs
                open_set.add(neighbor)
    return max(g_score.values())


def solve(graph, flows):
    distances = prune_stuck_valves(calculate_distances(graph), flows)
    
    def neighbors(node):
        current_valve, pressure, remaining_valves, remaining_minutes = node
        for rv in remaining_valves:
            rt = remaining_minutes - distances.get((current_valve, rv), inf) - 1
            if rt >= 0:
                g = calculate_gain(current_valve, rv, distances, remaining_minutes, flows)
                yield rv, pressure + g, tuple(x for x in remaining_valves if x != rv), rt
    def h(node):
        current_valve, pressure, remaining_valves, remaining_minutes = node
        return sum(calculate_gain(current_valve, v, distances, remaining_minutes, flows) for v in remaining_valves)
    def d(node):
        current_valve, pressure, remaining_valves, remaining_minutes = node
        return pressure

    start = 'AA', 0, tuple(v for v, f in flows.items() if f), 30
    return b_star(start, neighbors, d, h)


def calculate_gain(current_valve, to_valve, distances, remaining_minutes, flows):
    if (current_valve, to_valve) in distances:            
        t = max(0, remaining_minutes - distances[current_valve, to_valve] - 1)
        return flows[to_valve] * t
    return 0

print(solve(*parse(sys.stdin)))