import operator

f = open("input_day02.txt")
l = [int(n) for n in f.readline().strip().split(",")]
l[1] = 12
l[2] = 2;

#l = [1,1,1,4,99,5,6,0,99]
pos = 0;
while (l[pos] != 99):
    if l[pos] == 1:
        op = operator.add
    if l[pos] == 2:
        op = operator.mul

    l[l[pos + 3]] = op(l[l[pos + 1]], l[l[pos + 2]])
    pos += 4

print(l)
print(l[0])

