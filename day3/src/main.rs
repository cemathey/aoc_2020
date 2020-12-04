use std::env;
use std::fs;

const OCCUPIED: char = '#';

#[derive(Debug)]
struct Position {
    x: usize,
    y: usize,
    max_x: usize,
    max_y: usize,
}

impl Position {
    fn update_horizontal_position(&self, dx: usize) -> usize {
        // Handle falling off the right side of the terrain and wrap to the beginning since it repeats

        let mut new_x = self.x + dx;

        if new_x > self.max_x {
            new_x = new_x % self.max_x - 1;
        }

        new_x
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_name = &args[1];

    let file_contents = load_file(file_name);
    let (max_x, max_y) = find_terrain_size(&file_contents);

    // Horizontal / Vertical slopes to check
    let slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];

    // Tree count for each individual slope
    let mut tree_counts: Vec<usize> = Vec::new();

    for (x, y) in slopes.iter() {
        // Collect the number of trees for each slope
        tree_counts.push(count_trees(
            *x as usize,
            *y as usize,
            &file_contents,
            max_x,
            max_y,
        ));
    }

    // Find the product of all of our slopes
    let mut product = 1;

    for num in tree_counts {
        product *= num;
    }

    println!("Tree Counts: {:?}", product);
}

fn find_terrain_size(s: &str) -> (usize, usize) {
    // Find the dimensions of our terrain
    let max_y = s.split_whitespace().count() - 1;
    let max_x = s.find("\n").unwrap() - 1;

    (max_x, max_y)
}

fn load_file(file_name: &str) -> String {
    // Read the contents of the input file as a single string
    let contents = fs::read_to_string(file_name).expect("Can't open the file.");

    return contents;
}

fn count_trees(
    horz_slope: usize,
    vert_slope: usize,
    lines: &String,
    max_x: usize,
    max_y: usize,
) -> usize {
    let mut pos = Position {
        x: 0,
        y: 0,
        max_x,
        max_y,
    };
    let mut tree_count = 0;

    for (i, line) in lines.split_whitespace().enumerate() {
        // Only count every nth line to handle vertical offsets > 1
        if pos.y != i {
            continue;
        }

        let characters: Vec<char> = line.chars().collect();

        if characters[pos.x] == OCCUPIED {
            tree_count += 1;
        }

        // Update our position on the terrain map
        let new_x = pos.update_horizontal_position(horz_slope);

        pos.x = new_x;
        pos.y += vert_slope;
    }

    return tree_count;
}
