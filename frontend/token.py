class TokenType:
    def __init__(self, name: str, reges: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return f"TokenType(name='{self.name}', regex=r'{self.regex}')"

class Token:
    def __init__(self, type: TokenType, value: str, position: int, line: int = 1, column: int = 1, is_nullable: bool = False):
        self.type = type
        self.value = value
        self.position = position
        self.line = line
        self.column = column
        self.is_nullable = is_nullable

    def __repr__(self):
        return f"Token(type={self.type.name}, value='{self.value}', pos={self.position}, line={self.line}, col={self.column}, nullable={self.is_nullable})"


token_types_list = {
    'NUMBER': TokenType("NUMBER", r'-?\d+(\.\d+)?([eE][+-]?\d+)?'),
    'STRING': TokenType("STRING", r'\"[^\"\n]*\"|\'[^\'\n]*\''),
    'CHAR': TokenType("CHAR", r'\'[^\']?\''),  
    'VARIABLE': TokenType("VARIABLE", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b(?!\s*(?:))'),
    'TRUE': TokenType("TRUE", r'\btrue\b'), 
    'FALSE': TokenType("FALSE", r'\bfalse\b'),
    'NULL': TokenType("NULL", r'\bnull\b'),  

    'ASSIGN': TokenType("ASSIGN", r'='),
    'EQUAL': TokenType("EQUAL", r'=='),
    'NOT_EQUAL': TokenType("NOT_EQUAL", r'!='),
    'LESS': TokenType("LESS", r'<'),
    'GREATER': TokenType("GREATER", r'>'),
    'LESS_EQUAL': TokenType("LESS_EQUAL", r'<='),
    'GREATER_EQUAL': TokenType("GREATER_EQUAL", r'>='), 
    'PLUS': TokenType("PLUS", r'\+'),
    'MINUS': TokenType("MINUS", r'-'),
    'MULTIPLY': TokenType("MULTIPLY", r'\*'),
    'DIVIDE': TokenType("DIVIDE", r'/'),

    'SEMICOLON': TokenType("SEMICOLON", r';'),
    'COLON': TokenType("COLON", r':'),
    'COMMA': TokenType("COMMA", r','),
    'DOT': TokenType("DOT", r'\.'),
    'ARROW': TokenType("ARROW", r'->'),

    'LPAREN': TokenType("LPAREN", r'\('),
    'RPAREN': TokenType("RPAREN", r'\)'),
    'LBRACE': TokenType("LBRACE", r'\{'),
    'RBRACE': TokenType("RBRACE", r'\}'),
    'LBRACKET': TokenType("LBRACKET", r'\['),
    'RBRACKET': TokenType("RBRACKET", r'\]'),
}