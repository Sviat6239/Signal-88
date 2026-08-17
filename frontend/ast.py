from abc import ABC
from typing import List, Optional
from .token import Token, TokenType

class ExpressionNode(ABC):
    def __init__(self, line: int = 1, column: int = 1):
        self.line: int = line
        self.column: int = column