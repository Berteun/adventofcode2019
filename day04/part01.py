def valid(n):
    double = False
    prev = 10 
    while(n) > 0:
        rem = n % 10
        if rem > prev:
            return False
        if rem == prev:
            double = True
        prev = rem
        n //= 10
    return double

print(sum(valid(n) for n in range(152085,670283 + 1)))
