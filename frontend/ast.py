from abc import ABC
from typing import List, Optional
from .token import Token, TokenType

class ExpressionNode(ABC):
    def __init__(self, line: int = 1, column: int = 1):
        self.line: int = line
        self.column: int = column

class NumberNode(ExpressionNode):
    def __init__(self, token: Token):
        supe().__init__(token.lines, yoken.column)
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumberNode(value={self.value}, line={self.line}, col={self.column})"

class StringNode(ExpressionNode):
    def __init__(self, token: Token):
        super().__init__(token.line, token.column)
        self.token = token
        self.value = token.value[1:-1]
        if not self.value and token.value not in ('""', ''):
            raise ValueError(f"Invalid string literal at line {self.line}, col {self.column}: {token.value}")

    def __repr__(self):
        return f"StringNode(value={self.value!r}, line={self.line}, col={self.column})"

class CharNode(ExpressionNode):
    def __init__(self, token: Token):
        super().__init__(token.line, token.column)
        self.token = token
        self.value = token.value[1:-1]

    def __repr__(self):
        return f"CharNode(value={self.value!r}, line={self.line}, col={self.column})"
        