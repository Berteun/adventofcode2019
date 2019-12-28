import itertools
import sys
sys.path.append('..')
from intcode import IntCodeMachine, open_file


class MachineIO:
    def __init__(self, machine_queues, n, phase):
        self.queues = machine_queues
        self.output = [phase]
        self.n = n
        self.max_output = 0

    def oninput(self):
        return self.queues[(self.n - 1) % 5].output.pop(0)

    def onoutput(self, val):
        self.max_output = max(val, self.max_output)
        self.output.append(val)

def run():
    instructions = open_file("input_day07.txt")

    best = 0
    for perm in itertools.permutations([5,6,7,8,9]):
        machines = []
        machine_io = []
        for n in range(5):
            io = MachineIO(machine_io, n, perm[n])
            machine_io.append(io)
            machines.append(IntCodeMachine(instructions.copy(), io.oninput, io.onoutput))

        # Kick off signal, since the last machine feeds into the first, we put it there
        machine_io[-1].output.append(0)

        while not (all(machine.halted for machine in machines)):
            for machine, io in zip(machines, machine_io):
                while not machine.halted:
                    machine.step()
                    if io.output:
                        break;

        best = max(machine_io[-1].max_output, best)
    print(best)

if __name__ == '__main__':
    run()
