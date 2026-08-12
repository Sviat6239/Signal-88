use super::lexer::{Token, TokenKind};

use super::ast::*; 

pub struct Parser {
    tokens: Vec<Token>,
    current: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, current: 0 }
    }

    fn peek(&self) -> &Token {
        &self.tokens[self.current]
    }

    fn is_at_end(&self) -> bool {
        self.peek().kind == TokenKind::Eof
    }

    fn advance(&mut self) -> &Token {
        if !self.is_at_end() {
            self.current += 1;
        }
        &self.tokens[self.current - 1]
    }

    fn match_token(&mut self, kind: TokenKind) -> bool {
        if self.peek().kind == kind {
            self.advance();
            true
        } else {
            false
        }
    }

    pub fn parse(&mut self) -> Program {
        let mut statements = Vec::new();

        while !self.is_at_end() {
            if let Some(stmt) = self.parse_statement() {
                statements.push(stmt);
            } else {
                break;
            }
        }

        Program { statements }
    }

    fn parse_statement(&mut self) -> Option<Stmt> {
        if self.match_token(TokenKind::Let) {
            self.parse_var_decl()
        } else {
            let expr = self.parse_expression()?;
            self.match_token(TokenKind::Semicolon);
            Some(Stmt::Expr(expr))
        }
    }

    fn parse_var_decl(&mut self) -> Option<Stmt> {
        let is_mutable = self.match_token(TokenKind::Mut);

        let name = match &self.advance().kind {
            TokenKind::Ident(s) => s.clone(),
            _ => {
                eprintln!("Error: Expected variable name");
                return None;
            }
        };

        if !self.match_token(TokenKind::Equal) {
            eprintln!("Error: Expected '='");
            return None;
        }

        let initializer = self.parse_expression()?;
        self.match_token(TokenKind::Semicolon);

        Some(Stmt::VarDecl {
            name,
            is_mutable,
            initializer,
        })
    }

    pub fn parse_expression(&mut self) -> Option<Expr> {
        self.parse_addition()
    }

    fn parse_addition(&mut self) -> Option<Expr> {
        let mut expr = self.parse_multiplication()?;

        while matches!(self.peek().kind, TokenKind::Plus | TokenKind::Minus) {
            let op = match self.advance().kind {
                TokenKind::Plus => BinaryOpKind::Add,
                TokenKind::Minus => BinaryOpKind::Sub,
                _ => unreachable!(),
            };
            let right = self.parse_multiplication()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Some(expr)
    }

    fn parse_multiplication(&mut self) -> Option<Expr> {
        let mut expr = self.parse_primary()?;

        while matches!(self.peek().kind, TokenKind::Star | TokenKind::Slash) {
            let op = match self.advance().kind {
                TokenKind::Star => BinaryOpKind::Mul,
                TokenKind::Slash => BinaryOpKind::Div,
                _ => unreachable!(),
            };
            let right = self.parse_primary()?;
            expr = Expr::BinaryOp {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }

        Some(expr)
    }

    fn parse_primary(&mut self) -> Option<Expr> {
        let token = self.advance().clone();

        match token.kind {
            TokenKind::IntLiteral(val) => Some(Expr::IntLiteral(val)),
            TokenKind::StrLiteral(val) => Some(Expr::StrLiteral(val)),
            TokenKind::Ident(name) => Some(Expr::Variable(name)),
            TokenKind::LParen => {
                let expr = self.parse_expression()?;
                if !self.match_token(TokenKind::RParen) {
                    eprintln!("Error: Expected ')'");
                    return None;
                }
                Some(expr)
            }
            _ => {
                eprintln!("Error: Unexpected token {:?}", token.kind);
                None
            }
        }
    }
}