#!/usr/bin/python3

def read_input():
    f = open('input_day01.txt')
    return [int(l) for l in f]

def compute_fuel_needed_for_fuel(fuel):
    fuel_for_fuel = 0
    while fuel > 0:
        fuel = max((fuel // 3) - 2, 0)
        fuel_for_fuel += fuel
    return fuel_for_fuel

def compute_fuel_needed_for_modules(mass_list):
    total = 0
    for mass in mass_list:
        fuel_for_module = (mass // 3) - 2
        total += fuel_for_module + compute_fuel_needed_for_fuel(fuel_for_module)
    return total

def main():
    mass_list = read_input()
    fuel_needed = compute_fuel_needed_for_modules(mass_list)
    print(fuel_needed)

if __name__ == '__main__':
    main()
