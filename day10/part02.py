import math
import operator
from collections import defaultdict

visible = defaultdict(int)

def read_input():
    f = open("input_day10.txt")
    #f = open("example01.txt")
    #f = open("example02.txt")
    #f = open("easy.txt")
    grid = []
    for (i, l) in enumerate(f):
        grid.append([c == '#' for c in l.strip()])
    return grid

def enumerate_coords(grid, x, y):
    x += 1
    if x == len(grid[y]):
        x = 0
        y += 1
    while y < len(grid):
        yield (x, y)
        x += 1
        if x == len(grid[y]):
            x = 0
            y += 1

def lattice_points(x, y, xc, yc, g):
    xstep = (xc - x) // g
    ystep = (yc - y) // g

    for n in range(1, g + 1):
        yield (x + xstep * n, y + ystep * n)

def compute_visible(grid, x, y):
    for (xc, yc) in enumerate_coords(grid, x,y):
        g = math.gcd(xc - x, yc - y)
        for (lx, ly) in lattice_points(x, y, xc, yc, g):
            if grid[ly][lx]:
                if (ly == yc and lx == xc):
                    visible[(lx,ly)] += 1
                    visible[(x,y)] += 1
                    #print((lx,ly), " is visible from ", (x,y))
                break

def process(grid):
    for (y, row) in enumerate(grid):
        for (x, item) in enumerate(row):
            if grid[y][x]:
                compute_visible(grid, x, y)

def print_visible(grid):
    for (y, row) in enumerate(grid):
        for (x, item) in enumerate(row):
            print("{:3d}".format(visible[(x, y)]), sep=" ", end=" ")
        print()

def sorted_by_angle_and_dist(grid, loc):
    (xc, yc) = loc
    angles = []
    tau = 2 * math.pi
    for (y, row) in enumerate(grid):
        for (x, item) in enumerate(row):
            if not item:
                continue
            if (yc == y and xc == x):
                continue
            dy = yc - y
            dx = x - xc
            dist = math.sqrt(dy*dy + dx*dx)
            angles.append((round((-math.atan2(dy, dx) + math.atan2(1,0)) % tau, 4), dist, (x, y)))
    angles.sort()
    return angles

def pulverize_order(grid, loc):
    angles = sorted_by_angle_and_dist(grid, loc)
    grouped = []
    i = 0
    prev_angle = None
    while angles:
        if angles[i][0] != prev_angle:
            prev_angle = angles[i][0]
            grouped.append(angles.pop(i))
        else:
            i += 1

        if i == len(angles):
            prev_angle = None
            i = 0

    return grouped

porder = {}

def print_porder(grid):
    for (y, row) in enumerate(grid):
        for (x, item) in enumerate(row):
            if (x, y) in porder:
                print("{:3d}".format(1 + porder[(x, y)]), sep=" ", end=" ")
            else:
                print(" - ", sep=" ", end=" ")
        print()

def run():
    grid = read_input()
    process(grid)
    location = max(visible.items(), key=operator.itemgetter(1))[0]
    order = pulverize_order(grid, location)
    for (i, (angle, dist, (x,y))) in enumerate(order):
        porder[(x,y)] = i

    #print(order)
    print_porder(grid)

    sol = order[199][2][0] * 100 + order[199][2][1]
    print("Solution: ", sol)

if __name__ == '__main__':
    run()
