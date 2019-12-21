import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

# Jumps three steps
#
# So, jump if:
# We jump if we can land (D) AND !A or !B or !C ==> !(A AND B AND C) AND D 

input_string = """\
OR A T
AND B T
AND C T
NOT T J
AND D J
WALK
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
