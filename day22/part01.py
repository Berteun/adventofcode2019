from collections import deque
from enum import Enum
class Techniques(Enum):
    DEAL = 0,
    CUT  = 1,
    INCR = 2,

def read_input():
    f = open("input_day22.txt");
    #f = open("example01.txt")
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

def make_deck(n):
    return deque(range(n))

def shuffle(deck, instructions):
    for (instruction, count) in instructions:
        print(deck)
        if instruction == Techniques.DEAL:
            deck.reverse()
        if instruction == Techniques.CUT:
            if count > 0:
                cut = [deck.popleft() for _ in range(count)]
                deck.extend(cut)
            if count < 0:
                cut = [deck.pop() for _ in range(-count)]
                deck.extendleft(cut)
        if instruction == Techniques.INCR:
            new_deck = deque((None for _ in range(len(deck))))
            pos = 0
            for n in range(len(deck)):
                new_deck[pos] = deck[n]
                pos += count
                pos %= len(deck)
            deck = new_deck
    return deck

def run():
    instructions = read_input()
    deck = make_deck(10007)
    deck = shuffle(deck, instructions)
    print(deck.index(2019))

if __name__ == '__main__':
    run()
