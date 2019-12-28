import heapq
import itertools
from collections import deque, defaultdict

class DynamicGraph:
    def __init__(self, base_graph):
        self.graph = base_graph

    def neighbours(self, nodes, keys, prev):
        histories = [
            set(p[0] for p in prev),
            set(p[1] for p in prev),
            set(p[2] for p in prev),
            set(p[3] for p in prev),
        ]
        nbs = []
        for (i, node) in enumerate(nodes):
            neighbours = []
            for nb, (d, nb_doors) in self.graph[node].items():
                if nb in histories[i]:
                    continue
                keys_needed = set(d.lower() for d in nb_doors if 'A' <= d <= 'Z')
                if 'A' <= nb <= 'Z':
                    keys_needed.add(nb.lower())
                if keys.issuperset(keys_needed):
                    neighbours.append((nb, d))

            for (n, d) in neighbours:
                ncopy = list(nodes)
                ncopy[i] = n
                nbs.append((tuple(ncopy), d))
        return nbs

def read_input():
    f = open("input_day18_part2.txt")
    #f = open("example01_part2.txt")
    #f = open("example02_part2.txt")
    maze = [list(l.strip('\n')) for l in f]
    return maze

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

    #return { poi : (dist[pois[poi]], frozenset([rev_pois[q] for q in prev[pois[poi]] if q in rev_pois and 'A' <= rev_pois[q] <= 'Z'])) for poi in pois if pois[poi] in dist}
    result = {}
    for poi in pois:
        coord = pois[poi]
        if coord in dist:
            rev_list = [rev_pois[q] for q in prev[coord] if q in rev_pois]
            if len(list(key for key in rev_list if 'a' <= key <= 'z')) <= 2:
                result[poi] = (dist[pois[poi]], frozenset(p for p in rev_list if 'A' <= p <= 'Z'))
    return result


def dijkstra_all(maze, pois):
    rev_pois = { pois[poi] : poi for poi in pois }
    graph = {}
    for poi in pois:
        graph[poi] = dijkstra(maze, pois, rev_pois, poi)
    return graph

def print_graph(graph, pois):
    for (node) in graph:
        print("Node {}".format(node))
        for nb in sorted(graph[node]):
            dist, doors = graph[node][nb]
            print("    {}: {:3d}, Doors: {{{}}}".format(nb, dist, ', '.join(doors)))

def solve(full_graph, pois):
    dgraph = DynamicGraph(full_graph)
    keys = set()
    queue = []
    best_keys = {}
    start_node = ('1', '2', '3', '4')
    dist = { (start_node, frozenset() ) : 0 }
    prev =  { ( start_node, frozenset() ) : [] }
    heapq.heappush(queue, (0, frozenset(), start_node))
    count = 0
    all_keys = frozenset(k for k in pois if 'a' <= k <= 'z')
    while queue:
        count += 1
        d, keys, node = heapq.heappop(queue)
        if (node, keys) in dist and dist[(node, keys)] < d:
            continue
        for (nb, length) in dgraph.neighbours(node, keys, prev[(node, keys)]):
            key_nodes = { kn for kn in nb if 'a' <= kn <= 'z' }
            if key_nodes:
                new_keys = frozenset(keys | key_nodes)
            else:
                new_keys = keys.copy()
            if (nb, new_keys) not in dist or dist[(nb, new_keys)] > d + length:
                if new_keys not in best_keys or best_keys[new_keys] > d + length:
                    best_keys[new_keys] = d + length
                    dist[(nb, new_keys)] = d + length
                    prev[(nb, new_keys)] = prev[(node, keys)][:]
                    prev[(nb, new_keys)].append(node)
                    heapq.heappush(queue, (d + length, new_keys, nb))
    return dist,prev

def run():
    maze = read_input()
    graph, pois = build_graph(maze)
    full_graph = dijkstra_all(graph, pois)
    #print_graph(full_graph, pois)
    dist, prev = solve(full_graph, pois)
    all_keys = frozenset(k for k in pois if 'a' <= k <= 'z')
    all_routes = [(dist[poi, keys], prev[poi, keys], poi) for (poi, keys) in dist if keys == all_keys]

    best = min(all_routes)
    print("Best route {} steps, ends at {}".format(best[0], best[2]))

if __name__ == '__main__':
    run()
