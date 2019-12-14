import sys
sys.path.append("..")
from collections import defaultdict
from intcode import IntCodeMachine

def read_input():
    f = open("input_day13.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))


output = []

def run():
    memory = read_input()
    machine = IntCodeMachine(memory, None, output.append)
    machine.run()
    coords = defaultdict(int)
    for n in range(0, len(output), 3):
        x, y, t = output[n:n+3]
        coords[(x,y)] = t

    print(coords.values())
    print(len([t for t in coords.values() if t == 2]))

if __name__ == '__main__':
    run()
