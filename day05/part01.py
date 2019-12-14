import operator
import sys
sys.path.append("..")
from collections import defaultdict
from intcode import IntCodeMachine

def read_input():
    f = open("input_day05.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))

def run():
    result = []
    instructions = read_input();
    machine = IntCodeMachine(instructions, lambda : 1, result.append)
    machine.run()
    print(result[-1])

if __name__ == '__main__':
    run()
