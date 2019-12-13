import sys
sys.path.append("..")
from collections import defaultdict
from intcode import IntCodeMachine

def read_input():
    #f = open("cheats.txt")
    f = open("input_day13.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))


glyphs = {
    0: ' ',
    1: '█',
    2: '▒',
    3: '▂',
    4: '●',
}

output = []

def load_field(glyphs):
    minx = 999
    maxx = 0
    miny = 999
    maxy = 0

    for n in range(0, len(output), 3):
        (x, y, g) = output[n:n+3]
        minx = min(x, minx)
        maxx = max(x, maxx)
        miny = min(y, miny)
        maxy = max(y, maxy)

    maxx += 1
    maxy += 1

    field = [[None] * maxx for y in range(maxy)]
    for n in range(0, len(output), 3):
        (x, y, g) = output[n:n+3]
        field[y][x] = g

    return field

def draw_field(field):
    for row in field:
        print(''.join(glyphs[x] for x in row))


class Game:
    def __init__(self, field):
        self.field = field
        self.buffer = []
        self.paddle = None
        for y,row in enumerate(self.field):
            for x,g in enumerate(row):
                if g == 3:
                    self.paddle = (x,y)
                if g == 4:
                    self.ball = (x,y)

    def oninput(self):
        if self.paddle is None:
            return 0
        if self.paddle[0] < self.ball[0]:
            return 1
        elif self.paddle[0] > self.ball[0]:
            return -1
        return 0

    def onoutput(self, value):
        self.buffer.append(value)
        if len(self.buffer) == 3:
            x, y, glyph_or_score = self.buffer
            if x == -1:
                print("Score ", glyph_or_score)
            else:
                if glyph_or_score == 3:
                    self.paddle = (x,y)
                if glyph_or_score == 4:
                    self.ball = (x,y)
                self.field[y][x] = glyph_or_score
                draw_field(self.field)
            self.buffer = []

def run():
    memory = read_input()

    machine = IntCodeMachine(memory, None, output.append)
    machine.run()

    field = load_field(glyphs)
    memory = read_input()
    memory[0] = 2

    draw_field(field)
    game = Game(field)
    machine2 = IntCodeMachine(memory, game.oninput, game.onoutput)
    machine2.run()

if __name__ == '__main__':

    run()
