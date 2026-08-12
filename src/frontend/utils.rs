use std::fs;
use std::process;

pub fn read_file(filename: &str) -> String {
    match fs::read_to_string(filename) {
        Ok(content) => content,
        Err(err) => {
            eprintln!("Error opening file '{}': {}", filename, err);
            process::exit(1);
        }
    }
}