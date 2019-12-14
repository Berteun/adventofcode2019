import math
from collections import namedtuple, defaultdict
Element = namedtuple('Element','quantity name')
Reaction = namedtuple('Reaction', 'inputs outputs')

produced_by = defaultdict(list)
produced_of = {}

def to_element(s):
    qty, name = s.strip().split()
    return Element(int(qty), name)

def parse_reaction(l):
    inp, res = l.split('=>')
    inputs = [to_element(e) for e in inp.split(',')]
    output = to_element(res)
    return Reaction(inputs, output)

def read_input():
    f = open("input_day14.txt")
    #f = open("example04.txt")
    reactions = [parse_reaction(l.strip()) for l in f]
    return reactions


def setup_solver(reactions):
    for inputs, output in reactions:
        produced_by[output.name] = inputs
        produced_of[output.name] = output.quantity

def solve_recursively(element, quantity, inventory):
    if element == 'ORE':
        return quantity

    mult = int(math.ceil((quantity - inventory[element]) / produced_of[element]))
    inventory[element] = (produced_of[element] * mult - quantity)

    return sum(
        solve_recursively(source.name, source.quantity * mult, inventory)
        for source in produced_by[element]
    )

def run():
    reactions = read_input()
    system = setup_solver(reactions)

    trillion = 1000_000_000_000

    fuel1 = solve_recursively('FUEL', 1, defaultdict(int))
    lower = trillion // fuel1
    upper = 10*lower
    while lower < upper:
        mid = (upper + lower) // 2
        ore = solve_recursively('FUEL', mid, defaultdict(int))
        if ore > trillion:
            upper = mid - 1
        else:
            lower = mid + 1


    print('Part 01:', fuel1)
    print("Part 02: Solution: {} can produce {} fuel".format(lower, solve_recursively('FUEL', lower, defaultdict(int))))


if __name__ == '__main__':
    run()
