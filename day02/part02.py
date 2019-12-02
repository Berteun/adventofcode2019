import operator

f = open("input_day02.txt")
o = [int(n) for n in f.readline().strip().split(",")]

for noun in range(100):
    for verb in range(100):
        l = o[:]
        l[1] = noun
        l[2] = verb

        pos = 0;
        try:
            while l[pos] != 99:
                if l[pos] == 1:
                    op = operator.add
                if l[pos] == 2:
                    op = operator.mul

                l[l[pos + 3]] = op(l[l[pos + 1]], l[l[pos + 2]])
                pos += 4
            if l[0] == 19690720:
                print(100 * noun + verb)
        except IndexError:
            continue;
