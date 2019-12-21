import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

# The logic is as follows.
# If we would fall into a gap otherwise, we jump (NOT A T // OR T J)
# We jump early, that is a gap at B or C if we have an out, that is we can move to E or we can jump to H.
input_string = """\
OR B J
AND C J
NOT J J
AND D J
OR E T
OR H T
AND T J
NOT A T
OR T J
RUN
"""
inputs = [ord(c) for c in input_string]

def oninput():
    result = inputs.pop(0)
    sys.stdout.write(chr(result))
    return result

def onoutput(i):
    if i < 256:
        sys.stdout.write(chr(i))
    else:
        print(i)

def run():
    memory = open_file("input_day21.txt")
    machine = IntCodeMachine(memory, onread=oninput, onwrite=onoutput)
    machine.run()

if __name__ == '__main__':
    run()
