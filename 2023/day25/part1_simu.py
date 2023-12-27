import sys
from collections import defaultdict
import random

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

def step(graph, coordinates, repulsion=1, attraction=1, d_cutoff=10, dt=0.01):
    n2c = {n:x for x, n in coordinates}
    v = [0 for _ in coordinates]
    
    for i, (x, n) in enumerate(coordinates):
        j = i - 1
        while j >= 0 and abs(d := x - coordinates[j][0]) < d_cutoff:
            v[i] += repulsion / (d*d)
            j -= 1
        j = i + 1
        while j < len(coordinates) and abs(d := x - coordinates[j][0]) < d_cutoff:
            v[i] -= repulsion / (d*d)
            j += 1
        for m in graph[n]:
            d = n2c[m] - x
            v[i] += attraction * d
    
    next_coordinates = [(x + dt*v, n) for (v, (x, n)) in zip(v, coordinates)]
    return next_coordinates

def simulate(graph):
    '''
    Do a 1d physics simulation where vertices have repulsion forces
    (electric) and edges have attraction forces (hook).

    The system should find an equilibrium with the vertices in two
    clusters joined only by the 3 edges to cut.
    '''
    coordinates = [(random.random(), i) for i in graph]
    
    for i in range(100):
        coordinates.sort()
        easing = 10 / (1+i)
        coordinates = step(graph, coordinates, dt=easing, d_cutoff=10*easing)
    return sorted(coordinates)

def avg(series):
    return sum(series) / len(series)

def k_means_step(data, centroids):
    clusters = [[] for _ in centroids]
    for x in data:
        _, cluster_i = min(
            (abs(x - c), ic) for ic, c in enumerate(centroids) 
        )
        clusters[cluster_i].append(x)
    new_centroids = [avg(cluster) for cluster in clusters]
    return clusters, new_centroids

def k_means(data):
    centroids = min(data), max(data)
    previous_clusters = None
    clusters = k_means_step(data, centroids)
    while clusters != previous_clusters:
        previous_clusters = clusters
        clusters, centroids = k_means_step(data, centroids)
    return clusters

from pprint import pprint
def solve(graph):
    coordinates_and_nodes = simulate(graph)
    import pprint
    pprint.pprint(coordinates_and_nodes)
    coordinates = [c for c, _ in coordinates_and_nodes]
    clusters = k_means(coordinates)
    return len(clusters[0]) * len(clusters[1])

lines = sys.stdin.readlines()
graph = parse(lines)
pprint(solve(graph))