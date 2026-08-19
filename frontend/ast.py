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

class IfNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, then_branch: 'BlockNode', else_branch: Optional['BlockNode']):
        super().__init__(condition.line, condition.column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode({self.condition}, {self.then_branch}, {self.else_branch}, line={self.line}, col={self.column})"

class WhileNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: 'BlockNode'):
        super().__init__(condition.line, condition.column)
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body}, line={self.line}, col={self.column})"

class ForNode(ExpressionNode):
    def __init__(self, init: Optional[ExpressionNode], cond: Optional[ExpressionNode], step: Optional[ExpressionNode], body: 'BlockNode'):
        super().__init__(init.line if init else body.line, init.column if init else body.column)
        self.init = init
        self.cond = cond
        self.step = step
        self.body = body

    def __repr__(self):
        return f"ForNode({self.init}, {self.cond}, {self.step}, {self.body}, line={self.line}, col={self.column})"

class SwitchNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, cases: List['CaseNode'], default: Optional['BlockNode']):
        super().__init__(expression.line, expression.column)
        self.expression = expression
        self.cases = cases
        self.default = default

    def __repr__(self):
        return f"SwitchNode({self.expression}, {self.cases}, {self.default}, line={self.line}, col={self.column})"

class CaseNode(ExpressionNode):
    def __init__(self, value: ExpressionNode, body: ExpressionNode):
        super().__init__(value.line, value.column)
        self.value = value
        self.body = body

    def __repr__(self):
        return f"CaseNode({self.value}, {self.body}, line={self.line}, col={self.column})"

class BreakNode(ExpressionNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)

    def __repr__(self):
        return f"BreakNode(line={self.line}, col={self.column})"

class ContinueNode(ExpressionNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)

    def __repr__(self):
        return f"ContinueNode(line={self.line}, col={self.column})"

class PrintNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode):
        super().__init__(expression.line, expression.column)
        self.expression = expression

    def __repr__(self):
        return f"PrintNode({self.expression}, line={self.line}, col={self.column})"

class InputNode(ExpressionNode):
    def __init__(self, token: Token, prompt: Optional[ExpressionNode] = None):
        super().__init__(token.line, token.column)
        self.token = token
        self.prompt = prompt

    def __repr__(self):
        return f"InputNode(token={self.token}, prompt={self.prompt}, line={self.line}, col={self.column})"

class CmpNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operandA: ExpressionNode, operandB: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operandA = operandA
        self.operandB = operandB

    def __repr__(self):
        return f"CmpNode(target={self.target}, operandA={self.operandA}, operandB={self.operandB}, line={self.line}, col={self.column})"

class JmpNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JmpNode(target={self.target}, line={self.line}, col={self.column})"

class JneNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JneNode(target={self.target}, line={self.line}, col={self.column})"

class JeNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JeNode(target={self.target}, line={self.line}, col={self.column})"

class JgeNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JgeNode(target={self.target}, line={self.line}, col={self.column})"

class JgNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JgNode(target={self.target}, line={self.line}, col={self.column})"

class JleNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JleNode(target={self.target}, line={self.line}, col={self.column})"

class JlNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JlNode(target={self.target}, line={self.line}, col={self.column})"

class JaNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JaNode(target={self.target}, line={self.line}, col={self.column})"

class JaeNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JaeNode(target={self.target}, line={self.line}, col={self.column})"

class JbNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JbNode(target={self.target}, line={self.line}, col={self.column})"

class JbeNode(ExpressionNode):
    def __init__(self, target: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target

    def __repr__(self):
        return f"JbeNode(target={self.target}, line={self.line}, col={self.column})"

class MovNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, source: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.source = source

    def __repr__(self):
        return f"JlNode(target={self.target}, source={self.source}, line={self.line}, col={self.column})"

class AddNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operandA: ExpressionNode, operandB: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operandA = operandA
        self.operandB = operandB

    def __repr__(self):
        return f"AddNode(target={self.target}, operandA={self.operandA}, operandB={self.operandB}, line={self.line}, col={self.column})"

class SubNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operandA: ExpressionNode, operandB: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operandA = operandA
        self.operandB = operandB

    def __repr__(self):
        return f"SubNode(target={self.target}, operandA={self.operandA}, operandB={self.operandB}, line={self.line}, col={self.column})"

class MulNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operandA: ExpressionNode, operandB: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operandA = operandA
        self.operandB = operandB

    def __repr__(self):
        return f"MulNode(target={self.target}, operandA={self.operandA}, operandB={self.operandB}, line={self.line}, col={self.column})"
      
class DivNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operandA: ExpressionNode, operandB: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operandA = operandA
        self.operandB = operandB

    def __repr__(self):
        return f"DivNode(target={self.target}, operandA={self.operandA}, operandB={self.operandB}, line={self.line}, col={self.column})"

class SinNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operand: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operand = operand

    def __repr__(self):
        return f"SinNode(target={self.target}, operand={self.operand}, line={self.line}, col={self.column})"     

class CosNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operand: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operand = operand

    def __repr__(self):
        return f"CosNode(target={self.target}, operand={self.operand}, line={self.line}, col={self.column})" 

class TanNode(ExpressionNode):
    def __init__(self, target: ExpressionNode, operand: ExpressionNode):
        super().__init__(token.line, token.column)
        self.target = target
        self.operand = operand

    def __repr__(self):
        return f"TanNode(target={self.target}, operand={self.operand}, line={self.line}, col={self.column})" 

class BlockNode(ExpressionNode):
    def __init__(self, statements: List[ExpressionNode], line: int = 1, column: int = 1):
        super().__init__(statements[0].line if statements else line, statements[0].column if statements else column)
        self.statements = statements

    def __repr__(self):
        return f"BlockNode({self.statements}, line={self.line}, col={self.column})"

class StatementsNode(ExpressionNode):
    def __init__(self, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.code_strings: List[ExpressionNode] = []

    def add_node(self, node: ExpressionNode):
        self.code_strings.append(node)
        if self.line == 1 and self.column == 1 and hasattr(node, 'line') and hasattr(node, 'column'):
            self.line = node.line
            self.column = node.column

    def __repr__(self):
        return f"StatementsNode({self.code_strings}, line={self.line}, col={self.column})"

class ProgramNode(ExpressionNode):
    def __init__(self, statements: List[ExpressionNode], imports: List['ImportNode'] = None):
        imports = imports or []
        
        line = imports[0].line if imports else (statements[0].line if statements else 1)
        column = imports[0].column if imports else (statements[0].column if statements else 1)
        
        super().__init__(line, column)
        self.imports = imports
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements}, line={self.line}, col={self.column})"