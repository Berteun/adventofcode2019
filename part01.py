import itertools

def read_input():
    f = open("input_day16.txt")
    #f = open("example02.txt")
    l = f.readline().strip()
    print(len(l))
    return list(int(d) for d in l)

def _generate_multipliers(base_pattern, repeat):
    sub_i = 1
    n = 0
    while True:
        if sub_i >= repeat:
            n += 1
            n %= len(base_pattern)
            sub_i = 0
        yield base_pattern[n]
        sub_i += 1

multipliers = []
def fill_patterns(length, base_pattern):
    for i in range(length):
        multipliers.append(generate_multipliers(base_pattern, i + 1, length))

def generate_multipliers(base_pattern, repeat, max):
    sub_i = 1
    n = 0
    result = []
    while len(result) < max:
        if sub_i >= repeat:
            n += 1
            n %= len(base_pattern)
            sub_i = 0
        result.append(base_pattern[n])
        sub_i += 1
    return result

def apply_pattern(digits, base_pattern):
    result = []
    for i, x in enumerate(digits):
        s = sum(p*d for (p,d) in zip(multipliers[i][i:], digits[i:]) if p != 0)
        result.append(abs(s) % 10)
    return result

def run():
    digits = read_input()
    base_pattern = [0, 1, 0, -1]
    fill_patterns(len(digits), base_pattern)
    for n in range(101):
        print(n, ''.join(str(d) for d in digits[:8]))
        digits = apply_pattern(digits, base_pattern)

if __name__ == '__main__':
    run()
