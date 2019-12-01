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

fn compute_fuel(masses: Vec<u32>) -> u32 {
    let mut fuel = 0;
    for mass in masses {
        fuel += mass / 3 - 2;
    }
    return fuel;
}

fn main() {
    let mass_list = read_input();
    let fuel = compute_fuel(mass_list);
    println!("Part 01: {}", fuel);
}
