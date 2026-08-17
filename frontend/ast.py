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