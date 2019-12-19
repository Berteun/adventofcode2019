import math
import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file


def update_grid(x, y, v):
    print(x, y, ':', v)

# Found through trial
sl1   = 7586 / 10000
sl2   = 9238 / 10000
d = (sl2 - sl1)

# Solve:
# Square: 
# 0.7586*y .... 0.9238 * y
# 0.7586*(y + 99) + 0.9238 * (y + 99)
# 0.7586 * y + 99 * 0.7586 ==> 175 breed moet het zijn
# 175 breed => 175 / d  ~ y van 1059

def loop(memory):
    for u_y in range(1059 - 2, 1059 + 3):
        l_y = u_y + 99

        x = int(l_y * 0.7586)

        for l_x in range(x - 1, x + 2):
            r_x = l_x + 99

            outputs = []
            for x,y in [(l_x, u_y), (r_x, u_y), (l_x, l_y), (r_x, l_y)]:
                lst = [y, x]
                machine = IntCodeMachine(memory.copy(), lst.pop, outputs.append)
                machine.run()
                if (outputs == [1,1,1,1]):
                    return(l_x, u_y)

def run():
    memory = open_file("input_day19.txt")
    x, y = loop(memory)
    print(x, y, 10000 * x + y)

if __name__ == '__main__':
    run()
