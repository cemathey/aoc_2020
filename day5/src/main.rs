use std::env;
use std::fs;

const MAX_ROWS: usize = 128;
const MAX_COLS: usize = 8;

fn main() {
    // Snag the input passed as a command line argument
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];

    let file_string = fs::read_to_string(file_name).unwrap();

    // Vector of all of the seat IDs we calculate from the input 
    let mut seat_ids: Vec<usize> = Vec::new();

    // 2D vector to store which seats are empty/full on the plane
    let mut plane: Vec<Vec<usize>> = vec![vec![0; MAX_COLS]; MAX_ROWS];

    for line in file_string.lines() {
        let mut lower_row: usize = 0;
        let mut upper_row: usize = MAX_ROWS;
        let mut lower_col: usize = 0;
        let mut upper_col: usize = MAX_COLS;

        for character in line.chars() {
            let diff_row = upper_row - lower_row;
            let diff_col = upper_col - lower_col;

            match character {
                'F' => {
                    upper_row = lower_row + diff_row / 2;
                }
                'B' => {
                    lower_row = upper_row - diff_row / 2;
                }
                'L' => {
                    upper_col = lower_col + diff_col / 2;
                }
                'R' => {
                    lower_col = upper_col - diff_col / 2;
                }
                _ => (),
            };
        }

        // Occupied seats are set to 1
        plane[lower_row][lower_col] = 1;

        let seat_id = lower_row * 8 + lower_col;
        seat_ids.push(seat_id);
    }


    println!("Part 1: {}", seat_ids.iter().max().unwrap());

    // Find the only row that has a missing seat (sums to 7) and then find the empty column
    for (row_idx, row) in plane.iter().enumerate() {
        let row_sum: usize = row.iter().sum();

        if row_sum == 7 {
            let col_idx = row.iter().position(|num| num == &0).unwrap();
            println!("Part 2: {}", row_idx * 8 + col_idx);
        }    
    }

}
