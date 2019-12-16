import itertools

def read_input():
    f = open("input_day16.txt")
    l = f.readline().strip()
    offset = int(l[:7])
    return offset, list(int(d) for d in l)

# Observations:
# First n digits are always 0, so given the offset
# it is not influenced by any preceding digits, so we
# only care about the digits from offset.
#
# Secondly: The pattern at that time start with 'offset'
# number of 1s, which means its only 1s at that point.
#
# So the value for data[offset] is the sum of all the digits
# following it. data[offset + 1] will be the same, but - data[offset],
# since that now gets a 0 multiplier.
def compute(offset, digits):
    data = (digits * 10_000)[offset:]
    for n in range(100):
        s = sum(data)
        for i, d in enumerate(data):
            data[i] = s % 10
            s -= d
    print(''.join(str(d) for d in data[:8]))

def run():
    offset, digits = read_input()
    compute(offset, digits)

if __name__ == '__main__':
    run()
