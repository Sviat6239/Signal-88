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
    ImMut,
    Func,
    Enum,
    Struct,
    If,
    Else,
    Return,
    Print,
    PrtLn,
    Read,
    Add,
    Sub,
    Mul,
    Div,
    Sqrt,
    Root,
    Sin,
    Cos,
    Tan,
    Ctg,
    ArcSin,
    ArcCos,
    ArcTan,
    ArcCtg,
    Log,
    LogTen,
    Pow,
    Tetr,
    Fact,
    Label,
    Cmp,
    Jmp,
    Je,
    Jne,
    Jg,
    Jge,
    Jl,
    Jle,
    For,
    While,
    Switch,
    Case,

    I8,
    UI8,
    I16,
    UI16,
    I32,
    UI32,
    I64,
    UI64,
    F32,
    F64,
    Char,
    Str,

    Ident(String),
    IntLiteral(i64),
    StrLiteral(String),

    Plus,
    PlusPlus,
    PlusEqual,
    Minus,
    MinusMinus,
    MinusEqual,
    Star,
    Slash,
    BackSlash,
    Equal,
    EqualEqual,
    Greater,
    Less,
    GreaterEqual,
    LessEqual,
    NotEqual,

    Exclamation,
    Question,

    Semicolon,
    Colon,
    LParen,
    RParen,
    LBrace,
    RBrace,
    LBracket,
    RBracket,

    Ampersand,
    Pipe,
    PipePipe,
    Arrow,
    Hash,
    Tilde,
    Percent,
    Dollar,
    At,
    Comma,
    Underscore,
    LArrow,
    RArrow,

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

            '*' => { tokens.push(Token::new(TokenKind::Star, line, column)); chars.next(); column += 1; }
            '/' => { tokens.push(Token::new(TokenKind::Slash, line, column)); chars.next(); column += 1; }
            ';' => { tokens.push(Token::new(TokenKind::Semicolon, line, column)); chars.next(); column += 1; }
            ':' => { tokens.push(Token::new(TokenKind::Colon, line, column)); chars.next(); column += 1; }
            '(' => { tokens.push(Token::new(TokenKind::LParen, line, column)); chars.next(); column += 1; }
            ')' => { tokens.push(Token::new(TokenKind::RParen, line, column)); chars.next(); column += 1; }
            '{' => { tokens.push(Token::new(TokenKind::LBrace, line, column)); chars.next(); column += 1; }
            '}' => { tokens.push(Token::new(TokenKind::RBrace, line, column)); chars.next(); column += 1; }
            '[' => { tokens.push(Token::new(TokenKind::LBracket, line, column)); chars.next(); column += 1; }
            ']' => { tokens.push(Token::new(TokenKind::RBracket, line, column)); chars.next(); column += 1; }
            '&' => { tokens.push(Token::new(TokenKind::Ampersand, line, column)); chars.next(); column += 1; }           
            '#' => { tokens.push(Token::new(TokenKind::Hash, line, column)); chars.next(); column += 1; }
            '~' => { tokens.push(Token::new(TokenKind::Tilde, line, column)); chars.next(); column += 1; }
            '@' => { tokens.push(Token::new(TokenKind::At, line, column)); chars.next(); column += 1; }
            ',' => { tokens.push(Token::new(TokenKind::Comma, line, column)); chars.next(); column += 1; }
            '_' => { tokens.push(Token::new(TokenKind::Underscore, line, column)); chars.next(); column += 1; }
            
            '=' => {
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'=') {
                    chars.next();
                    column += 1;
                    tokens.push(Token::new(TokenKind::EqualEqual, line, start_col));
                } else if chars.peek() == Some(&'>') {
                    chars.next();
                    column += 1;
                    tokens.push(Token::new(TokenKind::Arrow, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Equal, line, start_col));
                }
            }

            '!' => {
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'=') {
                    chars.next();
                    column += 1;
                    tokens.push(Token::new(TokenKind::NotEqual, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Exclamation, line, start_col));
                }
            }

            '-' =>{
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'-'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::MinusMinus, line, start_col));
                } else if chars.peek() == Some(&'='){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::MinusEqual, line, start_col));
                } else if chars.peek() == Some(&'>'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::RArrow, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Minus, line, start_col));
                }
            }
            
            '+' =>{
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'+'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::PlusPlus, line, start_col));
                } else if chars.peek() == Some(&'='){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::PlusEqual, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Plus, line, start_col));
                }
            }

            '<' =>{
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'<'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::LArrowLArrow, line, start_col));
                } else if chars.peek() == Some(&'='){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::LessEqual, line, start_col));
                } else if chars.peek() == Some(&'-'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::LArrow, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::Less, line, start_col));
                }
            }
            
            '>' =>{
                let start_col = column;
                chars.next();
                column += 1;
                if chars.peek() == Some(&'>'){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::RArrowRArrow, line, start_col));
                } else if chars.peek() == Some(&'='){
                    chars.next();
                    column += 1;
                    rokens.push(Token::new(TokenKind::GreaterEqual, line, start_col));
                } else {
                    tokens.push(Token::new(TokenKind::greater, line, start_col));
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
                    "func" => TokenKind::Func,
                    "if" => TokenKind::If,
                    "else" => TokenKind::Else,
                    "return" => TokenKind::Return,
                    "imm" => TokenKind::ImMut,
                    "enum" => TokenKind::Enum,
                    "struct" => TokenKind::Struct,
                    "print" => TokenKind::Print,
                    "prtln" => TokenKind::PrtLn,
                    "read" => TokenKind::Read,
                    "add" => TokenKind::Add,
                    "sub" => TokenKind::Sub,
                    "mul" => TokenKind::Mul,
                    "div" => TokenKind::Div,
                    "sqrt" => TokenKind::Sqrt,
                    "root" => TokenKind::Root,
                    "sin" => TokenKind::Sin,
                    "cos" => TokenKind::Cos,
                    "Tan" => TokenKind::Tan,
                    "ctg" => TokenKind::Ctg,
                    "arc_sin" => TokenKind::ArcSin,
                    "arc_cos" => TokenKind::ArcCos,
                    "arc_tan" => TokenKind::ArcTan,
                    "arc_ctg" => TokenKind::ArcCtg,
                    "log" => TokenKind::Log,
                    "log_ten" => TokenKind::LogTen,
                    "pow" => TokenKind::Pow,
                    "tetr" => TokenKind::Tetr,
                    "fact" => TokenKind::Fact,
                    "label" => TokenKind::Label,
                    "cmp" => TokenKind::Cmp,
                    "jmp" => TokenKind::Jmp,
                    "je" => TokenKind::Je,
                    "jne" => TokenKind::Jne,
                    "jg" => TokenKind::Jg,
                    "jge" => TokenKind::Jge,
                    "jl" => TokenKind::Jl,
                    "jle" => TokenKind::Jle,
                    "for" => TokenKind::For,
                    "while" => TokenKind::While,
                    "switch" => TokenKind::Switch,
                    "case" => TokenKind::Case,
                    "i8" => TokenKind::I8,
                    "i16" => TokenKind::I16,
                    "i32" => TokenKind::I32,
                    "i64" => TokenKind::I64,
                    "ui8" => TokenKind::UI8,
                    "ui16" => TokenKind::UI16,
                    "ui32" => TokenKind::UI32,
                    "ui64" => TokenKind::UI64,
                    "f32" => TokenKind::F32,
                    "f64" => TokenKind::F64,
                    "char" => TokenKind::Char,
                    "str" => TokenKind::Str,
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