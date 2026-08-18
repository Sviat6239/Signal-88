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

class BooleanNode(ExpressionNode):
    def __init__(self, token: Token):
        super().__init__(token.line, token.column)
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"BooleanNode(value={self.value}, line={self.line}, col={self.column})"

class NullNode(ExpressionNode):
    def __init__(self, token: Token):
        super().__init__(token.line, token.column)
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NullNode(value={self.value}, line={self.line}, col={self.column})"

class UnaryOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode, is_postfix: bool = False):
        super().__init__(operator.line, operator.column)
        self.operator = operator
        self.operand = operand
        self.is_postfix = is_postfix

    def __repr__(self):
        return f"UnaryOperationNode(operator={self.operator}, operand={self.operand}, is_postfix={self.is_postfix}, line={self.line}, col={self.column})"

class BinaryOperationNode(ExpressionNode):
    def __init__(self, operator: Token, left_node: ExpressionNode, right_node: ExpressionNode):
        super().__init__(operator.line, operator.column)
        self.operator = operator
        self.left_node = left_node
        self.right_node = right_node

    def __repr__(self):
        return f"BinaryOperationNode({self.operator}, {self.left_node}, {self.right_node}, line={self.line}, col={self.column})"

class NullCoalesceNode(ExpressionNode):
    def __init__(self, left_node: ExpressionNode, right_node: ExpressionNode):
        super().__init__(left_node.line, left_node.column)
        self.left_node = left_node
        self.right_node = right_node

    def __repr__(self):
        return f"NullCoalesceNode({self.left_node}, {self.right_node}, line={self.line}, col={self.column})"

class VariableNode(ExpressionNode):
    def __init__(self, variable: Token):
        super().__init__(variable.line, variable.column)
        self.variable = variable
        if not variable.value.strip():
            raise ValueError(f"Empty variable identifier at line {self.line}, col {self.column}")

    def __repr__(self):
        return f"VariableNode(value={self.variable.value}, line={self.line}, col={self.column})"

class AssignNode(ExpressionNode):
    def __init__(self, token: Token, variable: VariableNode, expression: ExpressionNode):
        super().__init__(token.line, token.column)
        self.token = token
        self.variable = variable
        self.expression = expression

    def __repr__(self):
        return f"AssignNode({self.token}, {self.variable}, {self.expression}, line={self.line}, col={self.column})"

class VarDeclarationNode(ExpressionNode):
    def __init__(self, var_token: Token, mutability: Token, variable: VariableNode, type_token: Optional[Token], expr: Optional[ExpressionNode], modifiers: List[Token] = None):
        super().__init__(var_token.line, var_token.column)
        self.var_token = var_token
        self.mutability = mutability
        self.variable = variable
        self.type_token = type_token
        self.expr = expr
        self.modifiers = modifiers or []

    def __repr__(self):
        return f"VarDeclarationNode({self.var_token}, {self.mutability}, {self.variable}, {self.type_token}, {self.expr}, modifiers={self.modifiers}, line={self.line}, col={self.column})"
