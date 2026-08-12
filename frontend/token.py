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
