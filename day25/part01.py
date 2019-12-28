import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

def read_input():
    valid_command = False
    while not valid_command:
        command = input("> ")
        first_word = command.split(' ')[0]
        valid_command = first_word in ['north', 'east', 'west', 'south', 'drop', 'take', 'inv']
    return command + '\n';

class OnInput:
    def __init__(self):
        self.buffer = []

    def __call__(self):
        if not self.buffer:
            self.buffer = list(read_input())
        return ord(self.buffer.pop(0))

oninput = OnInput()

def onoutput(ch):
    sys.stdout.write(chr(ch))

def run():
    memory = open_file("input_day25.txt")
    machine = IntCodeMachine(memory, oninput, onoutput)
    machine.run()

if __name__ == '__main__':
    run()
