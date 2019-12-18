import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

input_string = "A,B,A,C,B,A,B,C,C,B\nL,12,L,12,R,4\nR,10,R,6,R,4,R,4\nR,6,L,12,L,12\nn\n";
inputs = [ord(c) for c in input_string]

def oninput():
    result = inputs.pop(0)
    sys.stdout.write(chr(result))
    return result

x = 0
y = 0
scaffold = [[]]
def onoutput(i):
    if i > 255:
        print("Dust ", i)
    else:
        sys.stdout.write(chr(i))

def run():
    memory = open_file("input_day17.txt")
    memory[0] = 2
    machine = IntCodeMachine(memory, onread=oninput, onwrite=onoutput)
    machine.run()
    for line in scaffold:
        print(''.join(line))

if __name__ == '__main__':
    run()
