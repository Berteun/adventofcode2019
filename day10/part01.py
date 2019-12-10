import math
import operator
from collections import defaultdict

visible = defaultdict(int)

def read_input():
    f = open("input_day10.txt")
    #f = open("example01.txt")
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

def run():
    grid = read_input()
    process(grid)
    print(max(visible.items(), key=operator.itemgetter(1)))
    print_visible(grid)

if __name__ == '__main__':
    run()
