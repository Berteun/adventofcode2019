import sys
sys.path.append("..")
from collections import defaultdict
from intcode import IntCodeMachine
from robot import Robot

def read_input():
    f = open("input_day11.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))

def run():
    memory = read_input()
    robot = Robot()
    robot.squares[robot.pos] = 1
    machine = IntCodeMachine(memory, robot.read, robot.instruct)
    machine.run()
    
    for y in range(6):
        print(''.join([' ', '█'][robot.squares[x + y * 1j]] for x in range(42)))

if __name__ == '__main__':
    run()
