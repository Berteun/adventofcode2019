#!/usr/bin/python3

def read_input():
    f = open('input_day01.txt')
    return [int(l) for l in f]

def compute_fuel_needed(mass_list):
    return [(m // 3) - 2 for m in mass_list]

def main():
    mass_list = read_input()
    fuel_list = compute_fuel_needed(mass_list)
    print(sum(fuel_list))

if __name__ == '__main__':
    main()
