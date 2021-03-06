import operator
from collections import defaultdict
from enum import Enum

Mode = Enum('Mode', 'POS IMM REL', start=0)
Opcode = Enum('Opcode', 'Add Mul Input Output JumpIfTrue JumpIfFalse LessThan Equals SetBase')

def open_file(filename):
    f = open(filename)
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))

class IntCodeMachine:
    def __init__(self, memory, onread=None, onwrite=lambda x: None):
        self.onread, self.onwrite  = onread, onwrite
        self.memory = memory
        self.pos, self.offset = 0, 0
        self.halted = False

    def decode_next(self, instruction):
        mode_code, opcode = divmod(instruction, 100)
        modes = [Mode((mode_code // 10**n) % 10) for n in range(3)]
        return Opcode(opcode), modes

    def step(self):
        opcode, modes = self.decode_next(self.memory[self.pos])
        self.pos += 1
        self.eval(opcode, modes)
        self.halted = (self.memory[self.pos] == 99)

    def run(self):
        while not self.halted:
            self.step()

    def get_arg(self, mode, val):
        if mode == Mode.POS:
            return self.memory[val]
        elif mode == Mode.IMM:
            return val
        else:
            return self.memory[self.offset + val]

    def get_args(self, n, modes):
        return tuple(self.get_arg(modes[i], self.memory[self.pos + i]) for i in range(n))

    def get_args_and_output(self, n, modes):
        args, addr = self.get_args(n, modes), self.memory[self.pos + n]
        oaddr = addr + (self.offset if modes[n] == Mode.REL else 0)
        return args + (oaddr,)

    def eval_op(self, operator, modes):
        (o1, o2, oaddr)  = self.get_args_and_output(2, modes)
        self.memory[oaddr] = int(operator(o1, o2))
        self.pos += 3

    def eval_jump(self, cond, modes):
        (arg, dest) = self.get_args(2, modes)
        self.pos = dest if bool(arg) == cond else self.pos + 2

    def eval_inp(self, modes):
        (oaddr,) = self.get_args_and_output(0, modes)
        self.memory[oaddr] = self.onread()
        self.pos += 1

    def eval_out(self, modes):
        self.onwrite(self.get_args(1, modes)[0])
        self.pos += 1

    def eval_set_base(self, modes):
        self.offset += self.get_args(1, modes)[0]
        self.pos += 1

    def eval(self, opcode, modes):
        if opcode == Opcode.Add:
            self.eval_op(operator.add, modes)
        elif opcode == Opcode.Mul:
            self.eval_op(operator.mul, modes)
        elif opcode == Opcode.LessThan:
            self.eval_op(operator.lt, modes)
        elif opcode == Opcode.Equals:
            self.eval_op(operator.eq, modes)
        elif opcode == Opcode.JumpIfTrue:
            self.eval_jump(True, modes)
        elif opcode == Opcode.JumpIfFalse:
            self.eval_jump(False, modes)
        elif opcode == Opcode.Input:
            self.eval_inp(modes)
        elif opcode == Opcode.Output:
            self.eval_out(modes)
        elif opcode == Opcode.SetBase:
            self.eval_set_base(modes)
