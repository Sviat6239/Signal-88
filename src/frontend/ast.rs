#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    IntLiteral(i64),
    Variable(String),
    BinaryOp {
        left: Box<Expr>,
        op: BinaryOpKind,
        right: Box<Expr>,
    },
}

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOpKind {
    Add,
    Sub,
    Mul,
    Div,
    Equal,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Stmt {
    VarDecl {
        name: String,
        is_mutable: bool,
        data_type: String,
        initializer: Expr,
    },
    Expr(Expr),
}

#[derive(Debug, Clone, PartialEq)]
pub struct Program {
    pub statements: Vec<Stmt>,
}