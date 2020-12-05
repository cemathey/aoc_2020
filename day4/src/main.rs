use regex::Regex;
use std::env;
use std::fs;

#[derive(Debug)]
enum HeightUnit {
    Inch,
    Centimeter,
    None,
}

#[derive(Debug)]
struct Passport {
    byr: i32,
    iyr: i32,
    eyr: i32,
    hgt: i32,
    height_unit: HeightUnit,
    hcl: String,
    ecl: String,
    pid: String,
    cid: String,
}

impl Passport {
    fn create_empty_passport() -> Passport {
        Passport {
            byr: 0,
            iyr: 0,
            eyr: 0,
            hgt: 0,
            height_unit: HeightUnit::None,
            hcl: "".to_string(),
            ecl: "".to_string(),
            pid: "".to_string(),
            cid: "".to_string(),
        }
    }

    fn parse_height(height: &str) -> Result<i32, std::num::ParseIntError> {
        // Parse the numeric portion of the height string, from the start to the first non number char
        let idx = height
            .find(|c: char| !c.is_numeric())
            .unwrap_or(height.len());
        height[0..idx].parse::<i32>()
    }

    fn parse_height_unit(height: &str) -> HeightUnit {
        // Parse the unit of measurement from the height string from the last number to the end
        let idx = height.find(|c: char| !c.is_numeric()).unwrap_or(0);

        match &height[idx..] {
            "cm" => HeightUnit::Centimeter,
            "in" => HeightUnit::Inch,
            _ => HeightUnit::None,
        }
    }

    fn update_field(mut self, field: &str, val: &str) -> Passport {
        // Update our passport struct based off the provided field/value pair
        match field {
            "byr" => self.byr = val.parse::<i32>().unwrap(),
            "iyr" => self.iyr = val.parse::<i32>().unwrap(),
            "eyr" => self.eyr = val.parse::<i32>().unwrap(),
            "hgt" => {
                self.hgt = Passport::parse_height(val).unwrap();
                self.height_unit = Passport::parse_height_unit(val);
            }
            "hcl" => self.hcl = val.to_string(),
            "ecl" => self.ecl = val.to_string(),
            "pid" => self.pid = val.to_string(),
            "cid" => self.cid = val.to_string(),
            _ => panic!("Should never reach this."),
        }

        return self;
    }

    fn build_passport(raw_passport: &str) -> Passport {
        let mut passport = Passport::create_empty_passport();
        for kv_pairs in raw_passport.split_whitespace() {
            let split_idx = kv_pairs.find(":").unwrap();
            let key = &kv_pairs[0..split_idx];
            let val = &kv_pairs[split_idx + 1..];
            passport = passport.update_field(key, val);
        }
        passport
    }

    fn valid_passport_part_1(passport: &Passport) -> bool {
        // If any portion of our passport has the default value then it was missing when parsed
        // and the passport is invalid
        if passport.byr == 0 || passport.iyr == 0 || passport.eyr == 0 || passport.hgt == 0 {
            return false;
        }

        if passport.hcl == "" || passport.ecl == "" || passport.pid == "" {
            return false;
        }

        true
    }

    fn valid_passport_part_2(passport: &Passport) -> bool {
        // Test each relevant field of our passport and determine if any of them are false
        let mut checks: Vec<bool> = Vec::new();

        checks.push(Passport::valid_byr(passport.byr));
        checks.push(Passport::valid_iyr(passport.iyr));
        checks.push(Passport::valid_eyr(passport.eyr));
        checks.push(Passport::valid_hgt(passport.hgt, &passport.height_unit));
        checks.push(Passport::valid_hcl(&passport.hcl));
        checks.push(Passport::valid_ecl(&passport.ecl));
        checks.push(Passport::valid_pid(&passport.pid));

        return !checks.contains(&false);
    }

    fn valid_byr(year: i32) -> bool {
        return year >= 1920 && year <= 2002;
    }

    fn valid_iyr(year: i32) -> bool {
        return year >= 2010 && year <= 2020;
    }

    fn valid_eyr(year: i32) -> bool {
        return year >= 2020 && year <= 2030;
    }

    fn valid_hgt(height: i32, unit: &HeightUnit) -> bool {
        match unit {
            HeightUnit::Centimeter => height >= 150 && height <= 193,
            HeightUnit::Inch => height >= 59 && height <= 76,
            _ => false,
        }
    }

    fn valid_hcl(hcl: &str) -> bool {
        let re = Regex::new(r"#[0-9a-f]{6}").unwrap();
        re.is_match(hcl)
    }

    fn valid_ecl(ecl: &str) -> bool {
        match ecl {
            "amb" => true,
            "blu" => true,
            "brn" => true,
            "gry" => true,
            "grn" => true,
            "hzl" => true,
            "oth" => true,
            _ => false,
        }
    }

    fn valid_pid(pid: &str) -> bool {
        let re = Regex::new(r"^[0-9]{9}$").unwrap();
        re.is_match(pid)
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];

    let file_string = fs::read_to_string(file_name).unwrap();
    let mut passports: Vec<Passport> = Vec::new();

    for passport_chunk in file_string.split_terminator("\n\n") {
        passports.push(Passport::build_passport(passport_chunk));
    }

    let (part1, part2) = count_valid_passports(&passports);
    println!("Part 1 has {} valid passports.", part1);
    println!("Part 2 has {} valid passports.", part2);
}

fn count_valid_passports(passports: &Vec<Passport>) -> (i32, i32) {
    let mut part_1_valid_passports = 0;
    let mut part_2_valid_passports = 0;

    for passport in passports {
        if Passport::valid_passport_part_1(passport) {
            part_1_valid_passports += 1;
        }

        if Passport::valid_passport_part_2(passport) {
            part_2_valid_passports += 1;
        }
    }

    (part_1_valid_passports, part_2_valid_passports)
}
