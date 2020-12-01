use std::env;
use std::fs;
use std::collections::HashMap;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];
    const SUM_TARGET: i32 = 2020;

    let contents = fs::read_to_string(file_name)
        .expect("Can't open the file.");

    let mut numbers: Vec<i32> = Vec::new();
    let mut dict: HashMap<i32, bool> = HashMap::new();

    for num in contents.split("\n") {
        let num: i32 = num.trim().parse().unwrap();
        numbers.push(num);
        dict.insert(num, true);
    }

    for num in numbers {
        let diff = SUM_TARGET - num;

        match dict.get(&diff) {
            Some(true) =>  {
                println!("Answer: {}", num * diff);
                break;
            }
            _ => print!(""),
        }
    }

}
