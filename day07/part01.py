import itertools
import sys
sys.path.append('..')
from intcode import IntCodeMachine, open_file

def run():
    best, best_perm = 0, None
    for perm in itertools.permutations([0,1,2,3,4]):
        result = [0]
        for phase in perm:
            input_list = [result.pop(), phase]
            instructions = open_file("input_day07.txt")
            IntCodeMachine(instructions, input_list.pop, result.append).run()

        if result[-1] > best:
            best, best_perm = result[-1], perm
            best_perm = perm

    print(best, best_perm)

if __name__ == '__main__':
    run()
