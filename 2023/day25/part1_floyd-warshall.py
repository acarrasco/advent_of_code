import sys
from collections import defaultdict
import math
import heapq

def parse_line(line):
    src, dsts = line.split(':')
    return src, dsts.split()

def parse(lines):
    graph = defaultdict(list)
    for line in lines:
        src, dsts = parse_line(line.strip())
        for dst in dsts:
            graph[src].append(dst)
            graph[dst].append(src)
    return graph

def explore(graph, start, visited, excluded_edges):
    visited.add(start)
    for node in graph[start]:
        if node not in visited and (start, node) not in excluded_edges:
            explore(graph, node, visited, excluded_edges)

def connected(graph, excluded_edges):
    start = next(n for n in graph)
    visited = set()
    explore(graph, start, visited, excluded_edges)
    return len(visited)

def used_edges_in_minimal_paths(graph):
    '''
    Basically a Floyd-Warshall algorithm
    but keep track of when an edge contributes to the minimal path
    '''
    distances = defaultdict(lambda: math.inf)
    paths = {}
    for i in graph:
        distances[i, i] = 0
        for j in graph[i]:
            distances[i, j] = 1
            paths[i,j] = (i, j)

    for k in graph:
        for i in graph:
            for j in graph:
                if distances[i, j] > distances[i, k] + distances[k, j]:
                    paths[i, j] = paths[i, k] + paths[k, j][1:]
    
    used_edges = defaultdict(int)
    for path in paths.values():
        for a, b in zip(path, path[1:]):
            used_edges[a, b] += 1
    return used_edges


def solve(graph):
    n = len(graph)
    edges = used_edges_in_minimal_paths(graph)
    most_used_edges = heapq.nlargest(6, edges, key=edges.get)
    size = connected(graph, most_used_edges)
    return size * (n - size)

lines = sys.stdin.readlines()
graph = parse(lines)
print(solve(graph))