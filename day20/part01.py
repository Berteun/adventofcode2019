from collections import defaultdict
import re

def read_input():
    f = open("input_day20.txt")
    #f = open("example01.txt")
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

def dijkstra(graph, start, end):
    q = [(start, 0)]
    dist = { start: 0 }

    while q:
        (node, d) = q.pop(0)
        if node in dist and dist[node] < d:
            continue
        for (nb, length) in graph[node].items():
            if nb not in dist or dist[nb] > d + length:
                dist[nb] = d + length
                q.append((nb, d + length))
    return dist[end]

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
    graph = build_graph(maze, portals)
    solution = dijkstra(graph, portals['AA'][0], portals['ZZ'][0])
    print(solution)

if __name__ == '__main__':
    run()
