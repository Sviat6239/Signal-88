use std::env;
use std::process;

mod frontend;

use frontend::lexer;
use frontend::utils;
use frontend::parser;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Error: No source file specified.");
        eprintln!("Usage: {} <filename>", args[0]);
        process::exit(1);
    }

    let filename = &args[1];

    let source_code = utils::read_file(filename);
    println!("Source code:\n{}\n", source_code);

    println!("Starting Lexer...");
    let tokens = lexer::lex(&source_code);
    
    println!("Tokens finished. Printing tokens:");
    println!("{:#?}", tokens);

    println!("\nStarting Parser...");
    let ast = parser::parse(&tokens);

    //println!("\nAST Tree:");
    //println!("{:#?}", ast);


}