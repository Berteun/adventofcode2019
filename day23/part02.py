import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

class NetworkInput:
    def __init__(self, n):
        self.n = n
        self.input_queue = [n]
        self.idle = False

    def get(self):
        if self.input_queue:
            return self.input_queue.pop(0)
        else:
            self.idle = True
            return -1

    def deliver(self, x, y):
        self.idle = False
        self.input_queue.extend([x,y])

class NAT:
    def __init__(self):
        self.last = None

    def deliver(self, x, y):
        print("Delivered to 255: ", x, y)
        self.last = (x, y)
        self.last_delivered = None

    def release(self, queue):
        queue.idle = False
        if self.last:
            x, y = self.last
            if self.last_delivered is not None and y == self.last_delivered[1]:
                print("Twice in a row", y)
                sys.exit(0)
            self.last_delivered = self.last
            queue.deliver(x,y)

class NetworkOutput:
    def __init__(self, input_queues, n):
        self.input_queues = input_queues
        self.output_queue = []
        self.n = False

    def put(self, value):
        self.input_queues[self.n].idle = False
        self.output_queue.append(value)
        if len(self.output_queue) == 3:
            dest, x, y = self.output_queue
            self.output_queue.clear()
            self.input_queues[dest].deliver(x, y)


def initialize_computers(memory, number, nat):
    computers = []
    input_queues = {}
    for n in range(number):
        in_queue = NetworkInput(n)
        out_queue = NetworkOutput(input_queues, n)
        input_queues[n] = in_queue
        computers.append(IntCodeMachine(memory.copy(), in_queue.get, out_queue.put))

    input_queues[255] = nat
    return computers, input_queues

def run():
    memory = open_file("input_day23.txt")
    nat = NAT()
    computers, queues = initialize_computers(memory, 50, nat)

    while True:
        for n in range(50):
            computers[n].step()
            if all(queues[n].idle for n in range(50)):
                nat.release(queues[0])

if __name__ == '__main__':
    run()
