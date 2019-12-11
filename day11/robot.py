from collections import defaultdict

class Robot:
    def __init__(self):
        self.pos = 0 + 0j
        self.direction = - 1j
        self.squares = defaultdict(int)
        self.mode = 0

    def turn_left(self):
        self.direction *= -1j

    def turn_right(self):
        self.direction *= 1j

    def move(self):
        self.pos += self.direction

    def read(self):
        return self.squares[self.pos]

    def instruct(self, value):
        if self.mode:
            [self.turn_left, self.turn_right][value]()
            self.move()
        else:
            self.squares[self.pos] = value
        self.mode = 1 - self.mode

