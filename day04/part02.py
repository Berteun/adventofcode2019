def valid(n):
    double = False
    same = 0
    prev = 10 
    while(n) > 0:
        rem = n % 10
        if rem > prev:
            return False
        if rem == prev:
            same += 1
        else:
            if same == 2:
                double = True
            same = 1
        prev = rem
        n //= 10
    return double or same == 2

print(sum(valid(n) for n in range(152085,670283 + 1)))
