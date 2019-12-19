import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

max_x = 50
max_y = 50
grid = [[None] * max_x for _ in range(max_y)]

def update_grid(x, y, v):
    grid[y][x] = v

def run():
    memory = open_file("input_day19.txt")
    for y in range(max_y):
        for x in range(max_x):
            lst = [y, x]
            print(lst)
            machine = IntCodeMachine(memory.copy(), lst.pop, lambda v: update_grid(x, y, v))
            machine.run()

    for line in grid:
        print(''.join(str(x) for x in line))

    print(sum(sum(line) for line in grid))

if __name__ == '__main__':
    run()
