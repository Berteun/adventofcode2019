import sys
sys.path.append("..")
from intcode import IntCodeMachine 
from collections import defaultdict

def read_input():
    f = open("input_day09.txt")
    #f = open("example03.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    #l = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    #l = [1102,34915192,34915192,7,4,7,99,0]
    #l = [104,1125899906842624,99]
    return defaultdict(int, enumerate(l))

def run():
    input_list = read_input()
    m = IntCodeMachine(input_list, lambda: 1, lambda x: sys.stdout.write(str(x)))
    m.run()
    print()

if __name__ == '__main__':
    run()
