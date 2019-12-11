import sys
from collections import defaultdict
from intcode import IntCodeMachine


class Robot:
    def __init__(self):
        self.pos = 0 + 0j
        self.direction = - 1j
        self.squares = defaultdict(int)
        self.mode = 0

    def turn_left(self):
        self.direction *= -1j

    def turn_right(self):
        self.direction *= 1j

    def move(self):
        self.pos += self.direction

    def read(self):
        return self.squares[self.pos]

    def instruct(self, value):
        if self.mode:
            [self.turn_left, self.turn_right][value]()
            self.move()
        else:
            self.squares[self.pos] = value
        self.mode = 1 - self.mode

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
