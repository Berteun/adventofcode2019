import math

class Moon:
    def __init__(self, coords):
        self.coords = coords
        self.velocity = [0, 0, 0]

    def adjust_from_other(self, other):
        for n in range(3):
            if (self.coords[n] < other.coords[n]):
                self.velocity[n] += 1
            elif (self.coords[n] > other.coords[n]):
                self.velocity[n] -= 1

    def apply_velocity(self):
        for i in range(3):
            self.coords[i] += self.velocity[i]

    def potential(self):
        return sum(abs(c) for c in self.coords)

    def kinetic(self):
        return sum(abs(v) for v in self.velocity)

    def __str__(self):
        return 'pos=<x={:3d}, y={:3d}, z={:3}>, vel=<x={:3d}, y={:3d}, z={:d}>'.format(*self.coords, *self.velocity)

def parse_body(line):
    return [int(c.split('=')[1]) for c in line[1:-1].split(',')]

def read_input():
    f = open("input_day12.txt")
    #f = open("example01.txt")
    #f = open("example02.txt")
    return [parse_body(l.strip()) for l in f]

def lcm(a, b):
    return (a * b) // math.gcd(a, b)

def lcm3(a, b, c):
    return lcm(lcm(a,b), c)

def run():
    bodies = read_input()
    moons = [Moon(body) for body in bodies]
    states = [set(), set(), set()]
    cycled = [None, None, None]

    while True:
        for n in range(3):
            n_state = tuple(moon.coords[n] for moon in moons) + tuple(moon.velocity[n] for moon in moons)
            if n_state in states[n]:
                cycled[n] = True
            else:
                states[n].add(n_state)

        if all(cycled):
            break

        for moon1 in moons:
            for moon2 in moons:
                moon1.adjust_from_other(moon2)
        for moon in moons:
            moon.apply_velocity()

    print(lcm3(*(len(state) for state in states)))

if __name__ == '__main__':
    run()
