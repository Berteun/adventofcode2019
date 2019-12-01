use std::cmp;
use std::fs::File;
use std::io::{prelude::*, BufReader};

fn read_input() -> Vec<u32> {
    let file = File::open("input_day01.txt").unwrap();
    let reader = BufReader::new(file);
    let mut vec = Vec::new();

    for line in reader.lines() {
        vec.push(line.unwrap().parse::<u32>().unwrap());
    }

    return vec;
}

fn compute_fuel(masses: &[u32]) -> u32 {
    let mut fuel = 0;
    for mass in masses {
        fuel += mass / 3 - 2;
    }
    return fuel;
}

fn fuel_for_fuel(mut fuel: u32) -> u32 {
    let mut fuel_for_fuel = 0;
    while fuel > 8 {
        fuel = cmp::max((fuel / 3) - 2, 0);
        fuel_for_fuel += fuel;
    }
    return fuel_for_fuel;
}

fn compute_fuel_with_fuel(masses: &[u32]) -> u32 {
    let mut fuel = 0;
    for mass in masses {
        let base_fuel = mass / 3 - 2;
        fuel += base_fuel + fuel_for_fuel(base_fuel)
    }
    return fuel;
}

fn main() {
    let mass_list = read_input();
    let fuel = compute_fuel(&mass_list);
    println!("Part 01: {}", fuel);
    let fuel_with_fuel = compute_fuel_with_fuel(&mass_list);
    println!("Part 02: {}", fuel_with_fuel);
}
