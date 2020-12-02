use std::env;
use std::fs;
use std::collections::HashMap;


fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];
    const SUM_TARGET: i32 = 2020;

    let contents = load_file(file_name);
    let (numbers, lookup) = build_lookups(&contents);

    let (num1, num2) = part1(&numbers, &lookup, SUM_TARGET);
    println!("Part1: {} * {} = {}", num1, num2, num1 * num2);
    let (num1, num2, num3) = part2(&numbers, &lookup, SUM_TARGET);
    println!("Part2: {} * {} * {} = {}", num1, num2, num3, num1*num2*num3)

}


fn load_file(file_name: &str) -> String {
    let contents = fs::read_to_string(file_name)
        .expect("Can't open the file.");

    return contents
}


fn build_lookups(s: &String) -> (Vec<i32>, HashMap<i32, bool>) {
    let mut numbers: Vec<i32> = Vec::new();
    let mut lookup: HashMap<i32, bool> = HashMap::new();

    for num in s.split("\n") {
        let num: i32 = num.trim().parse().unwrap();
        numbers.push(num);
        lookup.insert(num, true);
    }

    return (numbers, lookup)
}


fn part1(numbers: &Vec<i32>, lookup: &HashMap<i32, bool>, sum_target: i32) -> (i32, i32) {
    for num in numbers.iter() {
        let diff = sum_target - num;

        if lookup.contains_key(&diff) {
            return (*num, diff);
        }
    }

    return (-1, -1);

}

fn part2(numbers: &Vec<i32>, lookup: &HashMap<i32, bool>, sum_target: i32) -> (i32, i32, i32) {
    for num in lookup.keys() {
        let diff = sum_target - num;

        let (num1, num2) = part1(&numbers, &lookup, diff);
        if num1 != -1 && num2 != -1 {
            return (num1, num2, *num);
        }
        
    }

    (-1, -1, -1)
}