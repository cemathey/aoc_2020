use std::env;
use std::fs;
use regex::Regex;

#[derive(Debug)]
struct Password {
    min: usize,
    max: usize,
    requirement: String,
    password: String,
}


fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];

    let lines = load_file(file_name);
    let passwords = collect_passwords(&lines);

    let valid_passwords = count_valid_passwords(passwords);
    
    println!("{} valid passwords.", valid_passwords);

}


fn load_file(file_name: &str) -> String {
    let contents = fs::read_to_string(file_name)
        .expect("Can't open the file.");

    return contents;
}


fn collect_passwords(lines: &str) -> Vec<Password> {
    let pattern = Regex::new(r"(\d+)-(\d+)\s(.+):\s(.+)").unwrap();
    let mut passwords: Vec<Password> = Vec::new();

    for line in lines.split("\n") {
        let parts = pattern.captures(line).unwrap();
        passwords.push(Password {
            min: parts.get(1).unwrap().as_str().parse().unwrap(),
            max: parts.get(2).unwrap().as_str().parse().unwrap(),
            requirement: parts.get(3).unwrap().as_str().to_string(),
            password: parts.get(4).unwrap().as_str().to_string(),
        })
    }
    
    return passwords;
}


fn valid_password(password: Password) -> bool {

    let contains: Vec<&str> = password.password.matches(&password.requirement).collect();
    let len = contains.len();
    
    if len >= password.min && len <= password.max {
        return true;
    }

    false
}


fn count_valid_passwords(passwords: Vec<Password>) -> u32 {
    let mut count = 0;
        
    for password in passwords {
        if valid_password(password) == true {
            count += 1;
        }
    }

    return count;

}