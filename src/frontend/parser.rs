use std::collections::HashMap;
use crate::lexer::Token;
use crate::frontend::ast::Stmt;
use crate::lexer::TokenKind;
use crate::frontend::ast::Expr;
use crate::frontend::ast::BinaryOpKind;
use crate::frontend::ast::Program;

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
    symbol_table: HashMap<String, String>,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            pos: 0,
            symbol_table: HashMap::new(),
        }
    }

    pub fn parse(&mut self) -> Program {
        let mut statements = Vec::new();

        while self.current().kind != TokenKind::Eof {
            if let Some(stmt) = self.parse_statement() {
                statements.push(stmt);
            } else {
                break;
            }
        }

        Program { statements }
    }

    fn current(&self) -> &Token {
        &self.tokens[self.pos]
    }

    fn advance(&mut self) -> &Token {
        let tok = &self.tokens[self.pos];
        if tok.kind != TokenKind::Eof {
            self.pos += 1;
        }
        tok
    }

    pub fn parse_statement(&mut self) -> Option<Stmt> {
        match self.current().kind {
            TokenKind::Let => {
                self.advance();

                let is_mutable = if self.current().kind == TokenKind::Mut {
                    self.advance();
                    true
                } else {
                    false
                };

                let data_type = match &self.current().kind {
                    TokenKind::Ident(t) => {
                        let t_str = t.clone();
                        self.advance();
                        t_str
                    }
                    _ => "i32".to_string(),
                };

                let name = match &self.advance().kind {
                    TokenKind::Ident(s) => s.clone(),
                    _ => panic!("Expected variable name"),
                };

                if self.advance().kind != TokenKind::Equal {
                    panic!("Expected '='");
                }

                self.symbol_table.insert(name.clone(), data_type.clone());

                let initializer = self.parse_expression()?;

                if self.advance().kind != TokenKind::Semicolon {
                    panic!("Expected ';'");
                }

                Some(Stmt::VarDecl {
                    name,
                    is_mutable,
                    data_type,
                    initializer,
                })
            }

            _ => {
                let expr = self.parse_expression()?;
                if self.current().kind == TokenKind::Semicolon {
                    self.advance();
                }
                Some(Stmt::Expr(expr))
            }
        }
    }

    pub fn parse_expression(&mut self) -> Option<Expr> {
        let token = self.advance().clone();

        let mut left = match token.kind {
            TokenKind::IntLiteral(val) => Expr::IntLiteral(val),
            TokenKind::Ident(ref name) => {
                if !self.symbol_table.contains_key(name) {
                    panic!("Semantic error: variable '{}' used before declaration", name);
                }
                Expr::Variable(name.clone())
            }
            _ => return None,
        };

        while let Some(op) = self.match_binary_op(&self.current().kind) {
            self.advance();
            let right = self.parse_expression()?;
            
            left = Expr::binary(left, op, right);
        }

        Some(left)
    }

    fn match_binary_op(&self, kind: &TokenKind) -> Option<BinaryOpKind> {
        match kind {
            TokenKind::Plus => Some(BinaryOpKind::Add),
            TokenKind::Minus => Some(BinaryOpKind::Sub),
            TokenKind::Star => Some(BinaryOpKind::Mul),
            TokenKind::Slash => Some(BinaryOpKind::Div),
            TokenKind::EqualEqual => Some(BinaryOpKind::Equal),
            _ => None,
        }
    }
}

pub fn parse(tokens: &[Token]) -> Program {
    let mut parser = Parser::new(tokens.to_vec());
    parser.parse()
}