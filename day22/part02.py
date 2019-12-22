from collections import deque
from enum import Enum
class Techniques(Enum):
    DEAL = 0,
    CUT  = 1,
    INCR = 2,

def modinv(n, deck_size):
    # Fermat: n^deck_size = n % deck_size
    # but we want n^(-1) s.t. n^(-1) * n = 1 % deck_size, so:
    # n^(deck_size - 1) = 1 % deck_size
    # And therefore:
    # n^(deck_size - 2) * n = 1 % deck_size, so
    # n^(deck_size - 2) => our inverse (this is only if deck_size is prime)
    return pow(n, deck_size - 2, deck_size)

def read_input():
    f = open("input_day22.txt");
    instructions = []
    for l in f:
        parts = l.rstrip('\n').split(' ')
        if l.startswith('deal with'):
            instructions.append((Techniques.INCR, int(parts[-1])))
        if l.startswith('deal into'):
            instructions.append((Techniques.DEAL, None))
        if l.startswith('cut'):
            instructions.append((Techniques.CUT, int(parts[-1])))
    return instructions

def shuffle_forward(deck_size, card, instructions):
    position = card
    max_index = deck_size - 1
    for (instruction, count) in instructions:
        if instruction == Techniques.DEAL:
            position = max_index - position
        if instruction == Techniques.CUT:
            position = (position - count) % deck_size
        if instruction == Techniques.INCR:
            position = (position * count) % deck_size
    return position

def shuffle_backward(deck_size, card, instructions):
    instructions = reversed(instructions)
    position = card
    max_index = deck_size - 1
    for (instruction, count) in instructions:
        if instruction == Techniques.DEAL:
            position = max_index - position
        if instruction == Techniques.CUT:
            position = (position + count) % deck_size
        if instruction == Techniques.INCR:
            # We had:
            # pos_new = (pos_old * count) % deck_size,
            # so, reversing (all % deck_size)
            # pos_new * count^1 = pos_old * count * count^1
            # pos_old = pow_new * count^1
            count_inv = modinv(count, deck_size)
            position = (position * count_inv) % deck_size
    return position

def gen_shuffle_forward(deck_size, instructions):
    position = [1, 0] # Position either gets shifted (deal / cut) or multiplied
                      # (increase), so starting with general position p,
                      # we can say that p_new = a*p + b % deck_size
    max_index = deck_size - 1
    for (instruction, count) in instructions:
        if instruction == Techniques.DEAL:
            position[0] *= -1
            position[1] = max_index - position[1]
        if instruction == Techniques.CUT:
            position[1] = (position[1] - count)
        if instruction == Techniques.INCR:
            position[0] *= count
            position[1] *= count
    return [position[0] % deck_size, position[1] % deck_size]

def gen_shuffle_backward(deck_size, instructions):
    position = [1, 0] # Position either gets shifted (deal / cut) or multiplied
                      # (increase), so starting with general position p,
                      # we can say that p_new = a*p + b % deck_size
    max_index = deck_size - 1

    for (instruction, count) in reversed(instructions):
        if instruction == Techniques.DEAL:
            position[0] *= -1
            position[1] = max_index - position[1]
        if instruction == Techniques.CUT:
            position[1] = (position[1] + count)
        if instruction == Techniques.INCR:
            count_inv = modinv(count, deck_size)
            position[0] *= count_inv
            position[1] *= count_inv

    return [position[0] % deck_size, position[1] % deck_size]

def shuffle_n_times(shuffle_params, deck_size, n_shuffles):
    # Say, factor, offset = shuffle_params
    # One shuffle is:
    # end_pos = factor*start_pos + offset
    # Two shuffles are:
    # end_pos = factor*(factor*start_pos + offset) + offset
    #         = f^2*start_pos + r*offset + offset
    # Three shuffles are
    #         = f^3*start_pos + f^2*offset + r*offset + offset
    # So, n shuffles are:
    #         => f^n*start_pos + f^(n-1)*offset + f^(n-2)*offset + ... + offset
    # Now do the multiply by (f - 1)/(f - 1) trick for the terms without start_pos and we get:
    #         => f^n start_pos + (f^n*offset - offset)/(f - 1)
    # We can can compute (note that we need to use mod inverse again since we are working mod)
    factor, offset = shuffle_params
    return [   pow(factor, n_shuffles, deck_size),
            (((pow(factor, n_shuffles, deck_size) - 1) * offset) * modinv(factor  - 1, deck_size)) % deck_size,
           ]

def simple(instructions, deck_size, start):
    goes_to = shuffle_forward(deck_size, start, instructions)
    print("{} goes to {}".format(start, goes_to))
    reverse = shuffle_backward(deck_size, goes_to, instructions)
    print("{} goes back to {}".format(goes_to, reverse))

    params = gen_shuffle_forward(deck_size, instructions)
    print("{} goes to {}".format(start, (start*params[0] + params[1]) % deck_size))

    rparams = gen_shuffle_backward(deck_size, instructions)
    print("{} goes back to {}".format(goes_to, (goes_to*rparams[0] + rparams[1]) % deck_size))

def slow_forward(instructions, deck_size, start, iterations):
    pos = start
    for n in range(iterations):
        pos = shuffle_forward(deck_size, pos, instructions)
    print("{} goes to {} after {} iterations".format(start, pos, iterations))
    return pos

def fast_forward(instructions, deck_size, start, iterations):
    params = gen_shuffle_forward(deck_size, instructions)
    power_params = shuffle_n_times(params, deck_size, iterations)
    position = (start*power_params[0] + power_params[1]) % deck_size
    print("{} goes to {} after {} iteratons".format(start, position, iterations))
    return position

def repeated_forward(instructions, deck_size, start, iterations):
    slow_forward(instructions, deck_size, start, iterations)
    return fast_forward(instructions, deck_size, start, iterations)

def slow_backward(instructions, deck_size, start, iterations):
    pos = start
    iterations = 3
    for n in range(iterations):
        pos = shuffle_backward(deck_size, pos, instructions)
    print("{} goes backward to {} after {} iterations".format(start, pos, iterations))
    return pos

def fast_backward(instructions, deck_size, start, iterations):
    params = gen_shuffle_backward(deck_size, instructions)
    power_params = shuffle_n_times(params, deck_size, iterations)
    position = (start*power_params[0] + power_params[1]) % deck_size
    print("{} goes backward to {} after {} iteratons".format(start, position, iterations))
    return position

def repeated_backward(instructions, deck_size, start, iterations):
    slow_backward(instructions, deck_size, start, iterations)
    return fast_backward(instructions, deck_size, start, iterations)

def run():
    instructions = read_input()

    # Test 
    deck_size = 10007
    iterations = 3
    start = 2019

    simple(instructions, deck_size, start)
    goes_to = repeated_forward(instructions, deck_size, start, iterations)
    repeated_backward(instructions, deck_size, goes_to, iterations)

    deck_size = 119315717514047
    iterations = 101741582076661
    start = 2020

    print("\nPart 2:")
    pos = fast_backward(instructions, deck_size, start, iterations)
    print("Solution:", pos)

if __name__ == '__main__':
    run()
