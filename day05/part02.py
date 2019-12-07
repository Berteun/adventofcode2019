import operator

def comp_input():
    return 5
        
class OutputResult:
    def __init__(self):
        self.result = []

    def __call__(self, output):
        self.result.append(output)
output = OutputResult()


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
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] + r[1]
        machine.pos += self.arguments

class Mul:
    arguments = 3
    opcode = 2
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] * r[1]
        machine.pos += self.arguments

class Input:
    arguments = 1
    opcode = 3
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[0]] = comp_input()
        machine.pos += self.arguments


class Output:
    arguments = 1
    opcode = 4
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        output(r[0])
        machine.pos += self.arguments

class JumpIfTrue:
    arguments = 2
    opcode = 5
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
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
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
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
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
        vals = machine.get_args(self.arguments)
        array = machine.instructions
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = int(r[0] < r[1])
        machine.pos += self.arguments

class Equals:
    arguments = 3
    opcode = 5
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, machine):
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

    def get_args(self, n):
        return self.instructions[self.pos:self.pos + n]

    def step(self):
        if not self.halted:
            opcode = decode(self.instructions[self.pos])
            self.pos += 1
            opcode.eval(self)
            self.halted = (self.instructions[self.pos] == 99)

    
def decode(code):
    opcode = code % 100;
    code //= 100;
    args = []
    for n in range(opcodes[opcode].arguments):        
        mode = code % 10
        args.append(Argument(mode))
        code //= 10
    return opcodes[opcode](*args)

def read_input():
    f = open("input_day05.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return l

def run():
    instructions = read_input();
    machine = Machine(instructions)
    while not machine.halted:
        machine.step()

    print(output.result)

if __name__ == '__main__':
    run()
