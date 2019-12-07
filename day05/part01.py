import operator

def comp_input():
    return 1
        
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

    def eval(self, array, *vals):
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] + r[1]

class Mul:
    arguments = 3
    opcode = 2
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, array, *vals):
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        array[vals[2]] = r[0] * r[1]

class Input:
    arguments = 1
    opcode = 3
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, array, *vals):
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        print(r)
        array[vals[0]] = comp_input()


class Output:
    arguments = 1
    opcode = 4
    def __init__(self, *args):
        assert(len(args) == self.arguments)
        self.args = args

    def eval(self, array, *vals):
        r = [self.args[i].get(array, vals[i]) for i in range(self.arguments)]
        output(r[0])

opcodes = {
        1: Add,
        2: Mul,
        3: Input,
        4: Output,
}

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
    pos = 0
    while instructions[pos] != 99:
        opcode = decode(instructions[pos])
        pos += 1
        opcode.eval(instructions, *instructions[pos:pos + opcode.arguments])
        pos += opcode.arguments

    print(output.result)

if __name__ == '__main__':
    run()
