// https://adventofcode.com/2020/day/2

use std::env;
use std::fs;
use regex::Regex;

#[derive(Debug)]
struct Password {
    min: usize, // Either the min # of occurences or index 1
    max: usize, // Either the max # of occurences or index 2
    requirement: String, // Password requirement to count/match against
    password: String, // User's password
}


fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];

    let lines = load_file(file_name);
    let passwords = collect_passwords(&lines);

    let (part1_valid_passwords, part2_valid_passwords) = count_valid_passwords(&passwords);

    println!("Part1: {} valid passwords.", part1_valid_passwords);
    println!("Part2: {} valid passwords.", part2_valid_passwords);
}


fn load_file(file_name: &str) -> String {
    let contents = fs::read_to_string(file_name)
        .expect("Can't open the file.");

    return contents;
}


fn collect_passwords(lines: &str) -> Vec<Password> {
    // Match a password in the style of `1-3 a: abcde`
    let pattern = Regex::new(r"(\d+)-(\d+)\s(.+):\s(.+)").unwrap();
    let mut passwords: Vec<Password> = Vec::new();

    for line in lines.split("\n") {
        // Build a password from its component pieces for each line in the file
        let parts = pattern.captures(line).unwrap();

        passwords.push(Password {
            min: parts.get(1).unwrap().as_str().parse().unwrap(),
            max: parts.get(2).unwrap().as_str().parse().unwrap(),
            requirement: parts.get(3).unwrap().as_str().to_string(),
            password: parts.get(4).unwrap().as_str().to_string(),
        });
    }
    
    return passwords;
}


fn part1_valid_password(password: &Password) -> bool {
    // Build a vector of each substring in the password that matches the requirement
    let contains: Vec<&str> = password.password.matches(&password.requirement).collect();
    let len = contains.len();
    
    // A valid password contains the password requirement min <= count <= max times
    if len >= password.min && len <= password.max {
        return true;
    }

    false
}


fn part2_valid_password(password: &Password) -> bool {
    // Build a vector of each individual character in the password so we can index off it
    let characters: Vec<char> = password.password.chars().collect();

    // Test whether each index of the password matches the password requirement
    let pos1 = characters[password.min-1].to_string() == password.requirement;
    let pos2 = characters[password.max-1].to_string() == password.requirement;

    // A valid password is an exclusive or of the requirement at position 1 (min) and position 2 (max)
    return pos1 ^ pos2;
}


fn count_valid_passwords(passwords: &Vec<Password>) -> (u32, u32) {
    // Count the number of valid passwords for part 1 and part 2
    let mut part1_count = 0;
    let mut part2_count = 0;

    for password in passwords {
            if part1_valid_password(&password) == true {
                part1_count += 1;
            }

            if part2_valid_password(&password) == true {
                part2_count += 1;
            }
    }

    return (part1_count, part2_count);
}
