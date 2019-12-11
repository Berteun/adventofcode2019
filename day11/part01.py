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
    machine = IntCodeMachine(memory, robot.read, robot.instruct)
    machine.run()
    print(len(robot.squares))

if __name__ == '__main__':
    run()
