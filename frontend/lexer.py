import re
from typing import List, Optional, Dict, Tuple, Pattern
from dataclasses import dataclass
from enum import Enum
import logging
from .token import Token, TokenType, token_types_list, token_types
from .error import format_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LexerError(Exception):
    pass

class TokenCategory(Enum):
    KEYWORD = "keyword"
    OPERATOR = "operator"
    PUNCTUATION = "punctuation"
    LITERAL = "literal"
    IDENTIFIER = "identifier"
    TYPE = "type"
    WHITESPACE = "whitespace"
    COMMENT = "comment"

@dataclass
class TokenSpec:
    name: str
    token_type: TokenType
    regex: str
    category: TokenCategory
    skip: bool = False

class Lexer:
    TOKEN_SPECS: List[TokenSpec] = [
        TokenSpec("IF", token_types_list["IF"], r"if\b", TokenCategory.KEYWORD),  # Conditional branch statement
        TokenSpec("ELSE", token_types_list["ELSE"], r"else\b", TokenCategory.KEYWORD),  # Alternative conditional branch statement
        TokenSpec("WHILE", token_types_list["WHILE"], r"while\b", TokenCategory.KEYWORD),  # Conditional loop statement
        TokenSpec("FOR", token_types_list["FOR"], r"for\b", TokenCategory.KEYWORD),  # Iteration loop statement
        TokenSpec("SWITCH", token_types_list["SWITCH"], r"switch\b", TokenCategory.KEYWORD),  # Multi-way branch selection statement
        TokenSpec("CASE", token_types_list["CASE"], r"case\b", TokenCategory.KEYWORD),  # Branch condition inside a switch statement
        TokenSpec("DEFAULT", token_types_list["DEFAULT"], r"default\b", TokenCategory.KEYWORD),  # Fallback branch inside a switch statement
        TokenSpec("BREAK", token_types_list["BREAK"], r"break\b", TokenCategory.KEYWORD),  # Loop or switch execution exit
        TokenSpec("CONTINUE", token_types_list["CONTINUE"], r"continue\b", TokenCategory.KEYWORD),  # Skip to next loop iteration
        TokenSpec("RETURN", token_types_list["RETURN"], r"return\b", TokenCategory.KEYWORD),  # Return value from function
        TokenSpec("CMP", token_types_list["CMP"], r"cmp\b", TokenCategory.KEYWORD),  # Value comparison instruction
        TokenSpec("JMP", token_types_list["JMP"], r"jmp\b", TokenCategory.KEYWORD),  # Unconditional jump instruction
        TokenSpec("JNE", token_types_list["JNE"], r"jne\b", TokenCategory.KEYWORD),  # Jump if not equal instruction
        TokenSpec("JE", token_types_list["JE"], r"je\b", TokenCategory.KEYWORD),  # Jump if equal instruction
        TokenSpec("JLE", token_types_list["JLE"], r"jle\b", TokenCategory.KEYWORD),  # Jump if less or equal instruction
        TokenSpec("JL", token_types_list["JL"], r"jl\b", TokenCategory.KEYWORD),  # Jump if less instruction
        TokenSpec("JGE", token_types_list["JGE"], r"jge\b", TokenCategory.KEYWORD),  # Jump if greater or equal instruction
        TokenSpec("JG", token_types_list["JG"], r"jg\b", TokenCategory.KEYWORD),  # Jump if greater instruction
        TokenSpec("MOV", token_types_list["MOV"], r"mov\b", TokenCategory.KEYWORD),  # Move/assign value instruction
        TokenSpec("PRINT", token_types_list["PRINT"], r"print\b", TokenCategory.KEYWORD),  # Output to standard console statement
        TokenSpec("INPUT", token_types_list["INPUT"], r"input\b", TokenCategory.KEYWORD),  # Read from standard input statement
        TokenSpec("FUNCTION", token_types_list["FUNCTION"], r"func\b", TokenCategory.KEYWORD),  # Function declaration keyword
        TokenSpec("ENUM", token_types_list["ENUM"], r"enum\b", TokenCategory.KEYWORD),  # Enumeration declaration keyword
        TokenSpec("STRUCTURE", token_types_list["STRUCTURE"], r"struct\b", TokenCategory.KEYWORD),  # Structure declaration keyword
        TokenSpec("LET", token_types_list["LET"], r"let\b", TokenCategory.KEYWORD),  # Variable declaration keyword
        TokenSpec("ADD", token_types_list["ADD"], r"add\b", TokenCategory.KEYWORD),  # Addition instruction
        TokenSpec("SUB", token_types_list["SUB"], r"sub\b", TokenCategory.KEYWORD),  # Subtraction instruction
        TokenSpec("DIV", token_types_list["DIV"], r"div\b", TokenCategory.KEYWORD),  # Division instruction
        TokenSpec("MUL", token_types_list["MUL"], r"mul\b", TokenCategory.KEYWORD),  # Multiplication instruction
        TokenSpec("SIN", token_types_list["SIN"], r"sin\b", TokenCategory.KEYWORD),  # Sine mathematical function
        TokenSpec("COS", token_types_list["COS"], r"cos\b", TokenCategory.KEYWORD),  # Cosine mathematical function
        TokenSpec("TAN", token_types_list["TAN"], r"tan\b", TokenCategory.KEYWORD),  # Tangent mathematical function
        TokenSpec("CTG", token_types_list["CTG"], r"ctg\b", TokenCategory.KEYWORD),  # Cotangent mathematical function
        TokenSpec("ARCSIN", token_types_list["ARCSIN"], r"arc_sin\b", TokenCategory.KEYWORD),  # Arcsine mathematical function
        TokenSpec("ARCCOS", token_types_list["ARCCOS"], r"arc_cos\b", TokenCategory.KEYWORD),  # Arccosine mathematical function
        TokenSpec("ARCTAN", token_types_list["ARCTAN"], r"arc_tan\b", TokenCategory.KEYWORD),  # Arctangent mathematical function
        TokenSpec("ARCCTG", token_types_list["ARCCTG"], r"arc_ctg\b", TokenCategory.KEYWORD),  # Arccotangent mathematical function
        TokenSpec("ROOT", token_types_list["ROOT"], r"root\b", TokenCategory.KEYWORD),  # N-th root mathematical function
        TokenSpec("POWER", token_types_list["POWER"], r"pow\b", TokenCategory.KEYWORD),  # Exponentiation/power mathematical function
        TokenSpec("SQRT", token_types_list["SQRT"], r"sqrt\b", TokenCategory.KEYWORD),  # Square root mathematical function
        TokenSpec("FACTORIAL", token_types_list["FACTORIAL"], r"fact\b", TokenCategory.KEYWORD),  # Factorial mathematical function
        TokenSpec("TETRATION", token_types_list["TETRATION"], r"tetr\b", TokenCategory.KEYWORD),  # Tetration mathematical function
        TokenSpec("LOGARITHM", token_types_list["LOGARITHM"], r"log\b", TokenCategory.KEYWORD),  # Natural/custom base logarithm function
        TokenSpec("LOGARITHMTEN", token_types_list["LOGARITHMTEN"], r"log10\b", TokenCategory.KEYWORD),  # Base-10 logarithm function
        TokenSpec("PUSH", token_types_list["PUSH"], r"push\b", TokenCategory.KEYWORD),  # Stack push / collection append operation
        TokenSpec("POP", token_types_list["POP"], r"pop\b", TokenCategory.KEYWORD),  # Stack pop / collection extract operation
        TokenSpec("LABEL", token_types_list["LABEL"], r"label\b", TokenCategory.KEYWORD),  # Code jump label definition

        # Type Casts / Conversions
        TokenSpec("TOI8", token_types_list["TOI8"], r"\btoi8\b", TokenCategory.KEYWORD),  # Cast to 8-bit signed integer
        TokenSpec("TOI16", token_types_list["TOI16"], r"\btoi16\b", TokenCategory.KEYWORD),  # Cast to 16-bit signed integer
        TokenSpec("TOI32", token_types_list["TOI32"], r"\btoi32\b", TokenCategory.KEYWORD),  # Cast to 32-bit signed integer
        TokenSpec("TOI64", token_types_list["TOI64"], r"\btoi64\b", TokenCategory.KEYWORD),  # Cast to 64-bit signed integer
        TokenSpec("TOUI8", token_types_list["TOUI8"], r"\btoui8\b", TokenCategory.KEYWORD),  # Cast to 8-bit unsigned integer
        TokenSpec("TOUI16", token_types_list["TOUI16"], r"\btoui16\b", TokenCategory.KEYWORD),  # Cast to 16-bit unsigned integer
        TokenSpec("TOUI32", token_types_list["TOUI32"], r"\btoui32\b", TokenCategory.KEYWORD),  # Cast to 32-bit unsigned integer
        TokenSpec("TOUI64", token_types_list["TOUI64"], r"\btoui64\b", TokenCategory.KEYWORD),  # Cast to 64-bit unsigned integer
        TokenSpec("TOF32", token_types_list["TOF32"], r"\btof32\b", TokenCategory.KEYWORD),  # Cast to 32-bit float
        TokenSpec("TOF64", token_types_list["TOF64"], r"\btof64\b", TokenCategory.KEYWORD),  # Cast to 64-bit float
        TokenSpec("TOSTR", token_types_list["TOSTR"], r"\btostr\b", TokenCategory.KEYWORD),  # Cast to string
        TokenSpec("TOBIN", token_types_list["TOBIN"], r"\btobin\b", TokenCategory.KEYWORD),  # Cast to binary string representation
        TokenSpec("TOOCT", token_types_list["TOOCT"], r"\btooct\b", TokenCategory.KEYWORD),  # Cast to octal string representation
        TokenSpec("TOHEX", token_types_list["TOHEX"], r"\btohex\b", TokenCategory.KEYWORD),  # Cast to hexadecimal string representation

        TokenSpec("MUT", token_types_list["MUT"], r"mut\b", TokenCategory.TYPE),  # Mutable variable specifier
        TokenSpec("IMM", token_types_list["IMM"], r"imm\b", TokenCategory.TYPE),  # Immutable variable specifier
        TokenSpec("I8", token_types_list["I8"], r"i8\b", TokenCategory.TYPE),  # 8-bit signed integer type
        TokenSpec("I16", token_types_list["I16"], r"i16\b", TokenCategory.TYPE),  # 16-bit signed integer type
        TokenSpec("I32", token_types_list["I32"], r"i32\b", TokenCategory.TYPE),  # 32-bit signed integer type
        TokenSpec("I64", token_types_list["I64"], r"i64\b", TokenCategory.TYPE),  # 64-bit signed integer type
        TokenSpec("UI8", token_types_list["UI8"], r"ui8\b", TokenCategory.TYPE),  # 8-bit unsigned integer type
        TokenSpec("UI16", token_types_list["UI16"], r"ui16\b", TokenCategory.TYPE),  # 16-bit unsigned integer type
        TokenSpec("UI32", token_types_list["UI32"], r"ui32\b", TokenCategory.TYPE),  # 32-bit unsigned integer type
        TokenSpec("UI64", token_types_list["UI64"], r"ui64\b", TokenCategory.TYPE),  # 64-bit unsigned integer type
        TokenSpec("F32", token_types_list["F32"], r"f32\b", TokenCategory.TYPE),  # 32-bit floating-point type
        TokenSpec("F64", token_types_list["F64"], r"f64\b", TokenCategory.TYPE),  # 64-bit floating-point type
        TokenSpec("CHAR", token_types_list["CHAR"], r"char\b", TokenCategory.TYPE),  # Character type
        TokenSpec("STRING", token_types_list["STRING"], r"str\b", TokenCategory.TYPE),  # String type
        TokenSpec("LIST", token_types_list["LIST"], r"list\b", TokenCategory.TYPE),  # Dynamic list type
        TokenSpec("ARRAY", token_types_list["ARRAY"], r"array\b", TokenCategory.TYPE),  # Fixed-size array type
        TokenSpec("BOOL", token_types_list["BOOL"], r"bool\b", TokenCategory.TYPE),  # Boolean type
        TokenSpec("NULL", token_types_list["NULL"], r"null\b", TokenCategory.TYPE),  # Null/empty value type
        TokenSpec("VOID", token_types_list["VOID"], r"void\b", TokenCategory.TYPE),  # Void / no-return type

        # Memory Management & Low-level Operations
        TokenSpec("MALLOC", token_types_list["MALLOC"], r"\bmalloc\b", TokenCategory.KEYWORD),  # Allocate memory
        TokenSpec("CALLOC", token_types_list["CALLOC"], r"\bcalloc\b", TokenCategory.KEYWORD),  # Allocate and zero-initialize memory
        TokenSpec("REALLOC", token_types_list["REALLOC"], r"\brealloc\b", TokenCategory.KEYWORD),  # Reallocate memory block
        TokenSpec("FREE", token_types_list["FREE"], r"\bfree\b", TokenCategory.KEYWORD),  # Free allocated memory
        TokenSpec("MEMCPY", token_types_list["MEMCPY"], r"\bmemcpy\b", TokenCategory.KEYWORD),  # Memory copy
        TokenSpec("MEMMOVE", token_types_list["MEMMOVE"], r"\bmemmove\b", TokenCategory.KEYWORD),  # Memory move (safe for overlapping memory)
        TokenSpec("MEMSET", token_types_list["MEMSET"], r"\bmemset\b", TokenCategory.KEYWORD),  # Fill memory with constant byte
        TokenSpec("MEMCMP", token_types_list["MEMCMP"], r"\bmemcmp\b", TokenCategory.KEYWORD),  # Compare memory blocks
        TokenSpec("SIZEOF", token_types_list["SIZEOF"], r"\bsizeof\b", TokenCategory.KEYWORD),  # Size of data type or structure in bytes

        TokenSpec("NUMBER", token_types_list["NUMBER"], r"\d+(\.\d+)?([eE][+-]?\d+)?", TokenCategory.LITERAL),
        TokenSpec("STRING", token_types_list["STRING"], r"\"[^\"]*\"", TokenCategory.LITERAL),
        TokenSpec("CHAR", token_types_list["CHAR"], r"'[^']'", TokenCategory.LITERAL),
        TokenSpec("TRUE", token_types_list["TRUE"], r"true\b", TokenCategory.LITERAL),
        TokenSpec("FALSE", token_types_list["FALSE"], r"false\b", TokenCategory.LITERAL),
        TokenSpec("NULL", token_types_list["NULL"], r"null\b", TokenCategory.LITERAL),

        TokenSpec("SPACE", token_types_list["SPACE"], r"[ \t\r\n]+", TokenCategory.WHITESPACE, skip=True),
        TokenSpec("COMMENT", token_types_list["COMMENT"], r"#.*?$|/\*[\s\S]*?\*/", TokenCategory.COMMENT, skip=True),

        TokenSpec("VARIABLE", token_types_list["VARIABLE"], r"[a-zA-Z_][a-zA-Z0-9_]*", TokenCategory.IDENTIFIER),
    ]

    def __init__(self, code: str, filename: str, debug: bool = False):
        self.code = code.rstring() + "\n"
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.token_list: List[Token] = []
        self.debug = debug
        self.compiled_patterns: List[Tuple[TokenSpec, Pattern]] = [
            (spec, re.compile(r'^' + spec.regex, re.MULTILINE))
            for spec in self.TOKEN_SPECS
        ]

    def update_position(self, value: str) -> None:
        lines = value.split('\n')
        for i, line in enumerate(lines):
            if i < len(lines) - 1:
                self.line += 1
                self.column = 1
            else:
                self.column += len(line)
        self.pos += len(value)

    def lex_analysis(self) -> List[Token]:
        try:
            with open('tokens.log', 'w', encoding='utf-8') as f:
                while self.next_token():
                    token = self.token_list[-1]
                    f.write(f"Token: type={token.type.name}, value={token.value!r}, line={token.line}, column={token.column}\n")
                self.token_list.append(Token(token_types_list["EOF"], "", self.pos, self.line, self.column))
                f.write(f"Token: type=EOF, value='', line={self.line}, column={self.column}\n")
            self.validate_tokens()
            return [token for token in self.token_list if not self._is_skipped_token(token)]
        except LexerError as e:
            raise SyntaxError(str(e)) from e