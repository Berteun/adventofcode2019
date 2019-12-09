from collections import defaultdict
import itertools

class Argument:
    def __init__(self, mode):
        self.mode = mode

    def get(self, machine, val):
        if self.mode == 0:
            return machine.instructions[val]
        elif self.mode == 1:
            return val
        elif self.mode == 2:
            return machine.instructions[val + machine.offset]
        raise ValueError("Unsupported mode")

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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[2] if self.args[2].mode == 0 else vals[2] + machine.offset
        array[output_addr] = r[0] + r[1]
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[2] if self.args[2].mode == 0 else vals[2] + machine.offset
        array[output_addr] = r[0] * r[1]
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[0] if self.args[0].mode == 0 else vals[0] + machine.offset
        array[output_addr] = machine.get_input()
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[0] if self.args[0].mode == 0 else vals[0] + machine.offset
        machine.output(array[output_addr])
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[2] if self.args[2].mode == 0 else vals[2] + machine.offset
        array[output_addr] = int(r[0] < r[1])
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
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        output_addr = vals[2] if self.args[2].mode == 0 else vals[2] + machine.offset
        array[output_addr] = int(r[0] == r[1])
        machine.pos += self.arguments

class SetBase:
    arguments = 1
    opcode = 9
    def __init__(self, machine, *args):
        assert(len(args) == self.arguments)
        self.machine = machine
        self.args = args

    def eval(self):
        machine = self.machine
        vals = machine.get_args(self.arguments)
        r = [self.args[i].get(machine, vals[i]) for i in range(self.arguments)]
        machine.offset += r[0]
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
        9: SetBase
}

class Machine:
    def __init__(self, instructions):
        self.instructions = defaultdict(int)
        for (i, instr) in enumerate(instructions):
            self.instructions[i] = instr
        self.offset = 0
        self.pos = 0
        self.halted = False
        self.output_value = None
        self.result = []

    def get_args(self, n):
        return [self.instructions[x] for x in range(self.pos, self.pos + n)]

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
            opcode.eval()
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
                self.result.append(self.output_value)
                self.output_value = None

def read_input():
    f = open("input_day09.txt")
    #f = open("example03.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    #l = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    #l = [1102,34915192,34915192,7,4,7,99,0]
    #l = [104,1125899906842624,99]
    return l

def run():
    input_list = read_input()
    m = Machine(input_list[:])
    m.run([2])
    print(m.result)

if __name__ == '__main__':
    run()
