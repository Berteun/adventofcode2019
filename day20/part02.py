from collections import defaultdict
import re

def read_input():
    f = open("input_day20.txt")
    #f = open("example02.txt")
    return [l.strip('\n') for l in f]

def horizontal_portals(inp):
    portals = defaultdict(list)
    for (y,_) in enumerate(inp):
        for x in range(len(inp[y]) - 2):
            if inp[y][x].isalpha() and inp[y][x + 1].isalpha() and inp[y][x + 2] == '.':
                portals[inp[y][x:x+2]].append((x + 2,y))
            if inp[y][x] == '.' and inp[y][x + 1].isalpha() and inp[y][x + 2].isalpha():
                portals[inp[y][x+1:x+3]].append((x,y))
    return portals

def vertical_portals(inp):
    portals = defaultdict(list)
    for y in range(len(inp) - 2):
        for x in range(len(inp[y])):
            if inp[y][x].isalpha() and inp[y + 1][x].isalpha() and inp[y + 2][x] == '.':
                portals[inp[y][x] + inp[y + 1][x]].append((x, y + 2))
            if inp[y][x] == '.' and inp[y + 1][x].isalpha() and inp[y + 2][x].isalpha():
                portals[inp[y + 1][x] + inp[y + 2][x]].append((x,y))
    return portals


def process_input(inp):
    maze = {}
    zero = None
    for (i, l) in enumerate(inp):
        if zero is None and '#' in l:
            zero = (l.find('#'),i)
            break

    portals = defaultdict(list)
    hportals = horizontal_portals(inp)
    vportals = vertical_portals(inp)

    for ps in [hportals, vportals]:
        for elem in ps:
            for (x,y) in ps[elem]:
                portals[elem].append((x - zero[0],y - zero[0]))


    for (yc, l) in enumerate(inp):
        for (xc,c) in enumerate(l):
            y = yc - zero[1]
            x = xc - zero[0]
            if c in ['#', '.']:
                maze[(x,y)] = c

    return maze, portals

def get_neighbours(point, maze):
    (x, y) = point
    neighbours = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
    return [nb for nb in neighbours if nb in maze and maze[nb] == '.']

def search(point, maze, portals):
    portal_points = set()

    for l in portals.values():
        portal_points.update(l)

    edges = []
    seen = set([point])
    queue = [(0, point)]
    while queue:
        depth, p = queue.pop(0)
        nbs = [nb for nb in get_neighbours(p, maze) if not nb in seen]
        queue.extend([(depth + 1, nb) for nb in nbs])
        seen.update(nbs)
        if p in portal_points and p != point:
            edges.append([point, p, depth])
    return edges

def dijkstra(graph, start, end, portals):
    # Node, level, dist
    q = [(start, 0, 0)]
    dist = { (start, 0): 0 }
    prev = { (start, 0): None }
    done = False
    while q and not done:
        (node, level, d) = q.pop(0)
        #print(node, level, d)
        if (node, level) in dist and dist[(node, level)] < d:
            continue
        for nb, nb_level in graph.neighbours(level, node):
            length = graph.dist(node, nb)
            if (nb, nb_level) not in dist or dist[(nb, nb_level)] > d + length:
                dist[(nb, nb_level)] = d + length
                q.append((nb, nb_level, d + length))
                prev[(nb, nb_level)] = (node, level)
                if (nb == end):
                    print("Found: ", d + length)
                    done = False
    names = {}
    for (p,xl) in portals.items():
        for x in xl:
            names[x] = p

    #path = (end, 0)
    #while path is not None:
    #    print(path, names[path[0]])
    #    path = prev[path]

    return dist[(end, 0)]

class RecursiveGraph:
    def __init__(self, base, start, end):
        self.base = base
        self.start = start
        self.end = end
        self.max_x = max(n[0] for n in base)
        self.max_y = max(n[1] for n in base)

    def is_inner(self, node):
        (x, y) = node
        if x == 0 or y == 0:
            return False
        if x == self.max_x or y == self.max_y:
            return False
        return True

    def neighbours(self, level, node):
        nbs = []
        for (nb, dist) in self.base[node].items():
            if nb in [self.start, self.end] and level != 0:
                continue
            if (dist == 1):
                if self.is_inner(nb):
                    if level > 0:
                        nbs.append((nb, level - 1))
                elif level < 1000:
                    nbs.append((nb, level + 1))
            else:
                nbs.append((nb, level))
        return nbs

    def dist(self, fr, to):
        return self.base[fr][to]

def build_graph(maze, portals):
    edges = []
    for portal in portals:
        for (x, y) in portals[portal]:
            edges.extend(search((x,y), maze, portals))
    graph = defaultdict(lambda : defaultdict(int))
    for edge in edges:
        fr, to, dist = edge
        graph[fr][to] = dist

    for (portal, coords) in portals.items():
        if len(coords) != 2:
            continue
        fr, to = coords
        graph[fr][to] = 1
        graph[to][fr] = 1
    return graph

def run():
    inp = read_input()
    maze, portals = process_input(inp)
    base_graph = build_graph(maze, portals)
    recursive_graph = RecursiveGraph(base_graph, portals['AA'][0], portals['ZZ'][0])
    solution = dijkstra(recursive_graph, portals['AA'][0], portals['ZZ'][0], portals)
    print(solution)

if __name__ == '__main__':
    run()
