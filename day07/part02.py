import itertools

class Argument:
    def __init__(self, mode):
        self.mode = mode

    def get(self, array, val):
        if self.mode == 0:
            return array[val]
        else:
            return val

class Add:
    arguments = 3
    opcode = 1
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] + r[1]
        machine.pos += self.arguments

class Mul:
    arguments = 3
    opcode = 2
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] * r[1]
        machine.pos += self.arguments

class Input:
    arguments = 1
    opcode = 3
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[0]] = machine.get_input()
        machine.pos += self.arguments


class Output:
    arguments = 1
    opcode = 4
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        machine.output(r[0])
        machine.pos += self.arguments

class JumpIfTrue:
    arguments = 2
    opcode = 5
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        if (r[0] != 0):
            machine.pos = r[1]
        else:
            machine.pos += self.arguments

class JumpIfFalse:
    arguments = 2
    opcode = 5
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        if (r[0] == 0):
            machine.pos = r[1]
        else:
            machine.pos += self.arguments

class LessThan:
    arguments = 3
    opcode = 5
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = int(r[0] < r[1])
        machine.pos += self.arguments

class Equals:
    arguments = 3
    opcode = 5
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = int(r[0] == r[1])
        machine.pos += self.arguments

opcodes = {
        1: Add,
        2: Mul,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equals,
}

class Machine:
    def __init__(self, instructions):
        self.instructions = instructions
        self.pos = 0
        self.halted = False
        self.output_value = None

    def get_args(self, n):
        return self.instructions[self.pos:self.pos + n]

    def decode(self, code):
        opcode = code % 100;
        code //= 100;
        args = []
        for n in range(opcodes[opcode].arguments):        
            mode = code % 10
            args.append(Argument(mode))
            code //= 10
        return opcodes[opcode](self, *args)

    def step(self):
        if not self.halted:
            opcode = self.decode(self.instructions[self.pos])
            self.pos += 1
            try:
                opcode.eval()
            except:
                self.halted = True
                return
            self.halted = (self.instructions[self.pos] == 99)

    
    def get_input(self):
        return self.input.pop(0)
    
    def output(self, value):
        self.output_value = value

    def run(self, initial_input):
        self.input = initial_input[:]
        while not self.halted:
            self.step()
            if self.output_value:
                next_input = yield self.output_value
                self.output_value = None
                self.input.append(next_input)
        yield None

def read_input():
    f = open("input_day07.txt")
    #f = open("example03.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return l

def run():
    best = 0
    best_perm = None
    input_list = read_input()
    for perm in itertools.permutations([5,6,7,8,9]):
        machines = []
        generators = []
        for _ in range(5):
            machines.append(Machine(input_list[:]))

        prev = 0
        for i in range(5):
            generators.append(machines[i].run([perm[i], prev]))
            prev = next(generators[i])

        i = 0
        while not (all(machine.halted for machine in machines)):
            if not machines[i].halted:
                prev = generators[i].send(prev);

            if i == 4 and prev > best:
                best = prev
                best_perm = perm

            i = (i + 1) % 5

    print("best", best, best_perm)

if __name__ == '__main__':
    run()
