def read_input():
    return [l.strip().split(',') for l in open('input_day03.txt')]

def trace(d, start, end, ports, steps):
    while start != end:
        if start not in ports:
            ports[start] = steps
        steps += 1
        start += d

def parse_direction(instruction):
    deltas = { 'L': -1 + 0j, 'R': 1 + 0j, 'U': 0 + 1j, 'D': 0 -1j}
    d, dist = instruction[0], instruction[1:]
    return deltas[d], int(dist)

def cross_out_wire(w, pos, steps):
    ports = {}
    for instruction in w:
        direction, dist = parse_direction(instruction)
        end_pos = pos + dist * direction;
        trace(direction, pos, end_pos, ports, steps)
        steps, pos = steps + dist, end_pos
    return ports

def run():
    result = [cross_out_wire(w, 0 + 0j, 0) for w in read_input()]
    double = (set(result[0].keys()) & set(result[1].keys())) - {(0 + 0j)}
    print(min(result[0][c] + result[1][c] for c in double))
            
if __name__ == '__main__':
    run()
