from abc import ABC
from typing import List, Optional, Tuple
from .token import Token, TokenType, token_types_list
from .ast import (
    ExpressionNode, ProgramNode, BinaryOperationNode, NullCoalesceNode, NullNode,
    NumberNode, StringNode, CharNode, BooleanNode, BreakNode, UnaryOperationNode,
    VariableNode, AssignNode, VarDeclarationNode, IfNode, WhileNode, ForNode,
    SwitchNode, CaseNode, BreakNode, ContinueNode, PrintNode, InputNode, CmpNode,
    JmpNode, JneNode, JgeNode, JgNode, JaeNode, JaNode, JbeNode, JbNode, JeNode,
    JleNode, JlNode, MovNode, SubNode, MulNode, DivNode, SinNode, CosNode, TanNode,
    CtgNode, ArcCosNode, ArcCtgNode, ArcSinNode, ArcTanNode, RootNode, SqrtNode,
    FactorialNode, TetrationNode 
)
from .error import format_error
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Parser:
    """Parses a list of tokens into an AST for a strongly-typed language with Python-like imports."""
    def __init__(self, tokens: List[Token], source: str, filename: str, debug: bool = True):
        self.tokens = tokens
        self.source = source
        self.filename = filename
        self.pos = 0
        self.current_token: Optional[Token] = tokens[0] if tokens else None
        self.debug = debug
        if self.debug:
            logger.debug(f"Parser initialized with {len(tokens)} tokens")

    def advance(self) -> None:
        """Advances to the next token."""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        if self.debug:
            logger.debug(f"Advanced to token: {self.current_token.type.name if self.current_token else 'None'} at pos={self.pos}")

    def match(self, *token_types: TokenType) -> bool:
        """Checks if the current token matches any of the given token types and advances if matched."""
        if self.current_token and self.current_token.type in token_types:
            if self.debug:
                logger.debug(f"Matched token: {self.current_token.type.name}")
            self.advance()
            return True
        return False

    def expect(self, token_type_name: str) -> Token:
        """Expects a token of the given type, advances, and returns it; raises SyntaxError if not found."""
        if not self.current_token:
            raise SyntaxError(format_error(
                "SyntaxError",
                f"Expected {token_type_name}, got EOF",
                self.filename,
                self.source,
                self.tokens[-1].line if self.tokens else 1,
                self.tokens[-1].column if self.tokens else 1,
                token_length=1
            ))
        if self.current_token.type.name == token_type_name:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(format_error(
            "SyntaxError",
            f"Expected {token_type_name}, got {self.current_token.type.name}",
            self.filename,
            self.source,
            self.current_token.line,
            self.current_token.column,
            token_length=len(self.current_token.value) if self.current_token.value else 1
        ))
    
    def expect_one_of(self, token_type_names: Tuple[str, ...]) -> Token:
        """Expects one of the specified token types."""
        if not self.current_token:
            raise SyntaxError(format_error(
                "SyntaxError",
                f"Expected one of {token_type_names}, got EOF",
                self.filename,
                self.source,
                self.tokens[-1].line if self.tokens else 1,
                self.tokens[-1].column if self.tokens else 1,
                token_length=1
            ))
        if self.current_token.type.name in token_type_names:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(format_error(
            "SyntaxError",
            f"Expected one of {token_type_names}, got {self.current_token.type.name}",
            self.filename,
            self.source,
            self.current_token.line,
            self.current_token.column,
            token_length=len(self.current_token.value) if self.current_token.value else 1
        ))

    def parse(self) -> ProgramNode:
        """Parses the entire program into a ProgramNode with imports and statements."""
        return self.parse_program()

    def parse_program(self) -> ProgramNode:
        """Parses imports and statements into a ProgramNode."""
        imports = []
        statements = []
        while self.current_token and self.current_token.type.name != 'EOF':
            try:
                if self.match(token_types_list['IMPORT']):
                    imports.append(self.parse_import())
                else:
                    statements.append(self.parse_statement())
            except SyntaxError as e:
                logger.error(str(e))
                self.current_token = None
                break
        if self.debug:
            logger.debug(f"Parsed program: {len(imports)} imports, {len(statements)} statements")
        return ProgramNode(imports, statements)

    def parse_import(self) -> ImportNode:
        """Parses Python-style imports."""
        module = [self.expect('VARIABLE')]
        while self.current_token and self.current_token.type.name == 'DOT':
            self.advance()
            module.append(self.expect('VARIABLE'))
        names = []
        alias = None
        if self.current_token and self.current_token.type.name == 'FROM':
            self.advance()
            names = [self.expect('VARIABLE')]
            while self.current_token and self.current_token.type.name == 'COMMA':
                self.advance()
                names.append(self.expect('VARIABLE'))
            if self.current_token and self.current_token.type.name == 'AS':
                self.advance()
                alias = self.expect('VARIABLE')
        elif self.current_token and self.current_token.type.name == 'AS':
            self.advance()
            alias = self.expect('VARIABLE')
        self.expect('SEMICOLON')
        return ImportNode(module, names, alias)