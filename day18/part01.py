import heapq
from collections import deque, defaultdict

class DynamicGraph:
    def __init__(self, base_graph):
        self.graph = base_graph

    def neighbours(self, node, keys):
        neighbours = []
        for nb, (d, nb_preds) in self.graph[node].items():
            keys_needed = set(d.lower() for d in nb_preds if 'A' < d < 'Z')
            if keys.issuperset(keys_needed):
                neighbours.append((nb, d))
        return neighbours

def read_input():
    #f = open("input_day18.txt")
    #f = open("example01.txt")
    f = open("example02.txt")
    maze = [list(l.strip('\n')) for l in f]
    for (y, r) in enumerate(maze):
        if '@' in r:
            return maze, (r.index('@'), y)

def neighbours(maze, node):
    (x, y) = node
    neighbours = []
    if x > 0:
        neighbours.append((x - 1, y))
    if y > 0:
        neighbours.append((x, y - 1))
    if x < len(maze[0]) - 1:
        neighbours.append((x + 1, y))
    if y < len(maze) - 1:
        neighbours.append((x, y + 1))
    return [(nb_x, nb_y) for (nb_x, nb_y) in neighbours if maze[nb_y][nb_x] != '#']

def build_graph(maze):
    graph = defaultdict(lambda : defaultdict(int))
    pois = {}
    for (y, l) in enumerate(maze):
        for (x, c) in enumerate(l):
            if c not in ['#', '.']:
                pois[c] = (x, y)
            nbs = neighbours(maze, (x,y))
            for nb in nbs:
                graph[(x,y)][nb] = 1
    return graph, pois

# This is a bad Dijkstra
def dijkstra(graph, pois, rev_pois, start):
    q = [(pois[start], 0)]
    dist = { pois[start]: 0 }
    prev = { pois[start]: [] }
    while q:
        (node, d) = q.pop(0)
        if node in dist and dist[node] < d:
            continue
        for (nb, length) in graph[node].items():
            if nb not in dist or dist[nb] > d + length:
                dist[nb] = d + length
                prev[nb] = prev[node][:]
                prev[nb].append(node)
                q.append((nb, d + length))

    return { poi : (dist[pois[poi]], frozenset([rev_pois[q] for q in prev[pois[poi]] if q in rev_pois and 'a' <= rev_pois[q] <= 'z'])) for poi in pois }

def dijkstra_all(maze, pois):
    rev_pois = { pois[poi] : poi for poi in pois }
    graph = {}
    for poi in pois:
        graph[poi] = dijkstra(maze, pois, rev_pois, poi)
    return graph

def solve(full_graph, pois):
    dgraph = DynamicGraph(full_graph)
    keys = set()
    queue = []
    dist = { ('@', frozenset() ) : 0 }
    prev =  { ('@', frozenset() ) : [] }
    heapq.heappush(queue, (0, frozenset(), '@'))
    while queue:
        d, keys, node = heapq.heappop(queue)
        if (node, keys) in dist and dist[(node, keys)] < d:
            continue
        for (nb, length) in dgraph.neighbours(node, keys):
            if 'a' <= nb <= 'z':
                new_keys = frozenset(keys | set([nb]))
            if (nb, new_keys) not in dist or dist[(nb, new_keys)] > d + length:
                dist[(nb, new_keys)] = d + length
                prev[(nb, new_keys)] = prev[(node, keys)][:]
                prev[(nb, new_keys)].append(node)
                heapq.heappush(queue, (d + length, new_keys, nb))
    return dist,prev

def run():
    maze, start = read_input()
    graph, pois = build_graph(maze)
    print(pois)
    full_graph = dijkstra_all(graph, pois)
    dist, prev = solve(full_graph, pois)
    all_keys = frozenset(k for k in pois if 'a' <= k <= 'z')
    for (poi, keys) in dist:
        if all_keys == keys:
            print(poi, dist[poi, keys], prev[poi, keys])
if __name__ == '__main__':
    run()
