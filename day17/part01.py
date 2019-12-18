import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

x = 0
y = 0
scaffold = [[]]
def onoutput(i):
    global x
    global y
    if (i == 10):
        x = 0
        y += 1
        scaffold.append([])
    else:
        scaffold[y].append(chr(i))


def intersections():
    sum = 0
    for y in range(1, len(scaffold) - 1):
        for x in range(1, len(scaffold[y]) - 1):
            if scaffold[y][x] == '#' and scaffold[y][x - 1] == '#' and scaffold[y][x + 1] == '#' and scaffold[y - 1][x] == '#' and scaffold[y + 1][x] == '#':
                sum += (y * x)
    return sum

def run():
    memory = open_file("input_day17.txt")
    machine = IntCodeMachine(memory, None, onwrite=onoutput)
    machine.run()

    for line in scaffold:
        print(''.join(line))

    print(intersections())

if __name__ == '__main__':
    run()
