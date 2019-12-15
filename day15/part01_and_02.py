import operator
import sys
sys.path.append("..")
from collections import defaultdict, namedtuple
from intcode import IntCodeMachine
from enum import Enum

Tile = Enum('Tile', 'Unknown Empty Wall Oxygen', start=0)
Direction = Enum('Direction', 'North South West East')
StackFrame = namedtuple('StackFrame', ['position', 'direction', 'depth', 'reverse'])
tiles = {
    0: '?',
    1: ' ',
    2: '#',
    3: 'O',
}

offsets = {
    Direction.North: [ 0, -1],
    Direction.East:  [ 1,  0],
    Direction.West:  [-1,  0],
    Direction.South: [ 0,  1],
}

reverse = {
    Direction.North: Direction.South,
    Direction.East:  Direction.West,
    Direction.West:  Direction.East,
    Direction.South: Direction.North,
}

def draw_map(map, pos):
    print()
    minx = min(point[0] for point in map)
    miny = min(point[1] for point in map)

    maxx = max(point[0] for point in map) + 1
    maxy = max(point[1] for point in map) + 1

    for y in range(miny, maxy):
        for x in range(minx, maxx):
            if (x, y) == pos:
                sys.stdout.write('X')
            else:
                if (x, y) in map:
                    sys.stdout.write(tiles[map[(x,y)].value])
                else:
                    sys.stdout.write('?')
        sys.stdout.write('\n')

class Robot:
    def __init__(self):
        self.depth = 0
        self.pos = (0, 0)
        self.map = defaultdict(lambda: Tile.Empty)
        self.map[self.pos] = Tile.Empty
        self.stack = []
        self.start = True

    def oninput(self):
        if not self.stack:
            if self.start:
                self.start = False
                for direction in reversed([Direction.East, Direction.West, Direction.South, Direction.North]):
                    offset = offsets[direction]
                    target = (self.pos[0] + offset[0], self.pos[1] + offset[1])
                    self.stack.append(StackFrame(self.pos, direction, self.depth + 1, reverse[direction]))
            else:
                raise RuntimeError("Done!")
        return self.stack[-1].direction.value

    def onoutput(self, result):
        frame = self.stack[-1]
        offset = offsets[frame.direction]
        target = (self.pos[0] + offset[0], self.pos[1] + offset[1])

        self.stack.pop()
        if result == 0:
            self.map[target] = Tile.Wall
        else:
            if frame.reverse is not None:
                self.stack.append(StackFrame(self.pos, frame.reverse, frame.depth - 1, None))

            self.pos = target
            for direction in reversed([Direction.East, Direction.West, Direction.South, Direction.North]):
                offset = offsets[direction]
                new_target = (self.pos[0] + offset[0], self.pos[1] + offset[1])
                if not target in self.map:
                    self.stack.append(StackFrame(self.pos, direction, frame.depth + 1, reverse[direction]))

            self.depth = frame.depth

            if result == 1:
                self.map[target] = Tile.Empty
            elif result == 2:
                self.solution = self.depth
                self.oxygen = target
                self.map[target] = Tile.Oxygen
        #draw_map(self.map, self.pos)

def read_input():
    f = open("input_day15.txt")
    l = [int(n) for n in f.readline().strip().split(",")]
    return defaultdict(int, enumerate(l))

def fill_with_oxygen(oxygen_pos, map, minutes):
    if not oxygen_pos in map or map[oxygen_pos] == Tile.Wall or map[oxygen_pos] == Tile.Oxygen:
        return minutes - 1

    map[oxygen_pos] = Tile.Oxygen

    sol = 0
    for direction in [Direction.East, Direction.West, Direction.South, Direction.North]:
        offset = offsets[direction]
        target = (oxygen_pos[0] + offset[0], oxygen_pos[1] + offset[1])
        sol = max(fill_with_oxygen(target, map, minutes + 1), sol)
    return sol

def oxygen(map, oxygen_pos):
    sol = 0
    for direction in [Direction.East, Direction.West, Direction.South, Direction.North]:
        offset = offsets[direction]
        target = (oxygen_pos[0] + offset[0], oxygen_pos[1] + offset[1])
        sol = max(fill_with_oxygen(target, map, 1), sol)
    print("Part 2", sol)

def run():
    memory = read_input()
    robot = Robot()
    machine = IntCodeMachine(memory, robot.oninput, robot.onoutput)
    try:
        machine.run()
    except RuntimeError:
        print("Part 1", robot.solution, robot.oxygen)

    oxygen(robot.map, robot.oxygen)

if __name__ == '__main__':
    run()
