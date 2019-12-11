import sys
sys.path.append("..")
from intcode import IntCodeMachine 
from collections import defaultdict

def read_input():
    f = open("input_day09.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))

def run():
    input_list = read_input()
    m = IntCodeMachine(input_list, lambda: 2, lambda x: sys.stdout.write(str(x)))
    m.run()
    print()

if __name__ == '__main__':
    run()
