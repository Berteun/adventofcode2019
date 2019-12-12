
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
    return [parse_body(l.strip()) for l in f]

def run():
    bodies = read_input()
    moons = [Moon(body) for body in bodies]
    for step in range(1000):
        for moon in moons:
            print(str(moon))
        for moon1 in moons:
            for moon2 in moons:
                moon1.adjust_from_other(moon2)
        for moon in moons:
            moon.apply_velocity()

        print(sum(moon.potential() * moon.kinetic() for moon in moons))
if __name__ == '__main__':
    run()
