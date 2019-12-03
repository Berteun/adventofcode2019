def read_input():
    f = open('input_day03.txt')
    #return [['R8','U5','L5','D3'],['U7','R6','D4','L4']]
    #return [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
    #    ['U62','R66','U55','R34','D71','R55','D58','R83']]
    return [l.strip().split(',') for l in f]

def trace(d, start, end,ports):
    while start != end:
        ports.add(start)
        start = (start[0] + d[0], start[1] + d[1])
    ports.add(end)

def run():
    wires = read_input()
    result = []
    for w in wires:
        ports = set()
        pos = (0, 0)
        for direct in w:
            d = direct[0]
            dist = int(direct[1:])
            if d == 'U':
                npos = (pos[0], pos[1] + dist)
                trace((0,1), pos, npos,ports);
            elif d == 'L':
                npos = (pos[0] - dist, pos[1])
                trace((-1,0), pos, npos,ports);
            elif d == 'R':
                npos = (pos[0] + dist, pos[1])
                trace((1,0), pos, npos,ports);
            elif d =='D':
                npos = (pos[0], pos[1] - dist)
                trace((0,-1), pos, npos,ports);
            pos = npos
        result.append(ports)
    double = (result[0] & result[1]) - {(0,0)}
    print(min(abs(x) + abs(y) for (x,y) in double))
            
if __name__ == '__main__':
    run()
