import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine, open_file

class NetworkInput:
    def __init__(self, n):
        self.input_queue = [n]

    def get(self):
        if self.input_queue:
            return self.input_queue.pop(0)
        else:
            return -1

    def deliver(self, x, y):
        self.input_queue.extend([x,y])

class FinalQueue:
    def deliver(self, x, y):
        print("Delivered to 255: ", x, y)
        sys.exit(0)

class NetworkOutput:
    def __init__(self, input_queues):
        self.input_queues = input_queues
        self.output_queue = []

    def put(self, value):
        self.output_queue.append(value)
        if len(self.output_queue) == 3:
            dest, x, y = self.output_queue
            self.output_queue.clear()
            self.input_queues[dest].deliver(x, y)


def initialize_computers(memory, number):
    computers = []
    input_queues = {}
    for n in range(number):
        in_queue = NetworkInput(n)
        out_queue = NetworkOutput(input_queues)
        input_queues[n] = in_queue
        computers.append(IntCodeMachine(memory.copy(), in_queue.get, out_queue.put))

    input_queues[255] = FinalQueue()
    return computers

def run():
    memory = open_file("input_day23.txt")
    computers = initialize_computers(memory, 50)
    while True:
        for n in range(50):
            computers[n].step()

if __name__ == '__main__':
    run()
