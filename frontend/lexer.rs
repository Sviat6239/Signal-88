#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Span {
    pub line: usize,
    pub column: usize,
}

impl Span {
    pub fn new(line: usize, column: usize) -> Self {
        Self { line, column }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum TokenKind {
    Let,
    Mut,
    Fn,
    If,
    Else,
    Return,

    Ident(String),
    IntLiteral(i64),
    StrLiteral(String),

    Plus,
    Minus,
    Star,
    Slash,
    Assign,
    Equal,

    Semicolon,
    Colon,
    LParen,
    RParen,
    LBrace,
    RBrace,

    Eof,
    Unknown(char),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub kind: TokenKind,
    pub span: Span,
}

impl Token {
    pub fn new(kind: TokenKind, line: usize, column: usize) -> Self {
        Self {
            kind,
            span: Span::new(line, column),
        }
    }
}

pub struct TokenTable {
    pub tokens: Vec<Token>,
}

impl TokenTable {
    pub fn new() -> Self {
        Self { tokens: Vec::new() }
    }

    pub fn add(&mut self, kind: TokenKind, line: usize, column: usize) {
        self.tokens.push(Token::new(kind, line, column));
    }

    pub fn print_table(&self) {
        println!("{:<6} | {:<8} | {:<25}", "LINE", "COLUMN", "TOKEN KIND");
        println!("{:-<6}-+-{:-<8}-+-{:-<25}", "", "", "");

        for token in &self.tokens {
            println!(
                "{:<6} | {:<8} | {:?}",
                token.span.line,
                token.span.column,
                token.kind
            );
        }
    }
}

pub fn lex(source: &str) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut chars = source.chars().peekable();
    
    let mut line = 1;
    let mut column = 1;

    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' | '\r' => {
                chars.next();
                column += 1;
            }
            '\n' => {
                chars.next();
                line += 1;
                column = 1;
            }

            '+' => { tokens.push(Token::new(TokenKind::Plus, line, column)); chars.next(); column += 1; }
            '-' => { tokens.push(Token::new(TokenKind::Minus, line, column)); chars.next(); column += 1; }
            '*' => { tokens.push(Token::new(TokenKind::Star, line, column)); chars.next(); column += 1; }
            '/' => { tokens.push(Token::new(TokenKind::Slash, line, column)); chars.next(); column += 1; }
            ';' => { tokens.push(Token::new(TokenKind::Semicolon, line, column)); chars.next(); column += 1; }
            ':' => { tokens.push(Token::new(TokenKind::Colon, line, column)); chars.next(); column += 1; }
            '(' => { tokens.push(Token::new(TokenKind::LParen, line, column)); chars.next(); column += 1; }
            ')' => { tokens.push(Token::new(TokenKind::RParen, line, column)); chars.next(); column += 1; }
            '{' => { tokens.push(Token::new(TokenKind::LBrace, line, column)); chars.next(); column += 1; }
            '}' => { tokens.push(Token::new(TokenKind::RBrace, line, column)); chars.next(); column += 1; }

            '=' => {
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'=') {
                    chars.next();
                    column += 1;
                    tokens.push(Token::new(TokenKind::Equal, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Assign, line, start_col));
                }
            }

            'a'..='z' | 'A'..='Z' | '_' => {
                let start_col = column;
                let mut ident = String::new();

                while let Some(&ch) = chars.peek() {
                    if ch.is_alphanumeric() || ch == '_' {
                        ident.push(ch);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }

                let kind = match ident.as_str() {
                    "let" => TokenKind::Let,
                    "mut" => TokenKind::Mut,
                    "fn" => TokenKind::Fn,
                    "if" => TokenKind::If,
                    "else" => TokenKind::Else,
                    "return" => TokenKind::Return,
                    _ => TokenKind::Ident(ident),
                };

                tokens.push(Token::new(kind, line, start_col));
            }

            '0'..='9' => {
                let start_col = column;
                let mut num_str = String::new();

                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_digit() {
                        num_str.push(ch);
                        chars.next();
                        column += 1;
                    } else {
                        break;
                    }
                }

                let value = num_str.parse::<i64>().unwrap_or(0);
                tokens.push(Token::new(TokenKind::IntLiteral(value), line, start_col));
            }

            _ => {
                tokens.push(Token::new(TokenKind::Unknown(c), line, column));
                chars.next();
                column += 1;
            }
        }
    }

    tokens.push(Token::new(TokenKind::Eof, line, column));
    tokens
}