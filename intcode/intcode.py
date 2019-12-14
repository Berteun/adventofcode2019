import operator
from enum import Enum

Mode = Enum('Mode', 'POS IMM REL', start=0)
Opcode = Enum('Opcode', 'Add Mul Input Output JumpIfTrue JumpIfFalse LessThan Equals SetBase')

class IntCodeMachine:
    def __init__(self, instructions, onread=None, onwrite=lambda x: None):
        self.onread, self.onwrite  = onread, onwrite
        self.memory = instructions
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
        return {
            Mode.POS: lambda val: self.memory[val],
            Mode.IMM: lambda val: val,
            Mode.REL: lambda val: self.memory[self.offset + val],
        }[mode](val)

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
        return {
            Opcode.Add:      (lambda modes: self.eval_op(operator.add, modes)),
            Opcode.Mul:      (lambda modes: self.eval_op(operator.mul, modes)),
            Opcode.LessThan: (lambda modes: self.eval_op(operator.lt, modes)),
            Opcode.Equals:   (lambda modes: self.eval_op(operator.eq, modes)),
            Opcode.JumpIfTrue:  (lambda modes: self.eval_jump(True, modes)),
            Opcode.JumpIfFalse: (lambda modes: self.eval_jump(False, modes)),
            Opcode.Input:   self.eval_inp,
            Opcode.Output:  self.eval_out,
            Opcode.SetBase: self.eval_set_base,
        }[opcode](modes)
