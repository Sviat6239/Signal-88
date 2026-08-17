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
        TokenSpec("IF", token_types_list["IF"], r"if\b", TokenCategory.KEYWORD),
        TokenSpec("ELSE", token_types_list["ELSE"], r"else\b", TokenCategory.KEYWORD),
        TokenSpec("WHILE", token_types_list["WHILE"], r"while\b", TokenCategory.KEYWORD),
        TokenSpec("FOR", token_types_list["FOR"], r"for\b", TokenCategory.KEYWORD),
        TokenSpec("SWITCH", token_types_list["SWITCH"], r"switch\b", TokenCategory.KEYWORD),
        TokenSpec("CASE", token_types_list["CASE"], r"case\b", TokenCategory.KEYWORD),
        TokenSpec("DEFAULT", token_types_list["DEFAULT"], r"default\b", TokenCategory.KEYWORD),
        TokenSpec("BREAK", token_types_list["BREAK"], r"break\b", TokenCategory.KEYWORD),
        TokenSpec("CONTINUE", token_types_list["CONTINUE"], r"continue\b", TokenCategory.KEYWORD),
        TokenSpec("RETURN", token_types_list["RETURN"], r"return\b", TokenCategory.KEYWORD),
        TokenSpec("CMP", token_types_list["CMP"], r"cmp\b", TokenCategory.KEYWORD),
        TokenSpec("JMP", token_types_list["JMP"], r"jmp\b", TokenCategory.KEYWORD),
        TokenSpec("JNE", token_types_list["JNE"], r"jne\b", TokenCategory.KEYWORD),
        TokenSpec("JE", token_types_list["JE"], r"je\b", TokenCategory.KEYWORD),
        TokenSpec("JLE", token_types_list["JLE"], r"jle\b", TokenCategory.KEYWORD),
        TokenSpec("JL", token_types_list["JL"], r"jl\b", TokenCategory.KEYWORD),
        TokenSpec("JGE", token_types_list["JGE"], r"jge\b", TokenCategory.KEYWORD),
        TokenSpec("JG", token_types_list["JG"], r"jg\b", TokenCategory.KEYWORD),
        TokenSpec("MOV", token_types_list["MOV"], r"mov\b", TokenCategory.KEYWORD),
        TokenSpec("PRINT", token_types_list["PRINT"], r"print\b", TokenCategory.KEYWORD),
        TokenSpec("INPUT", token_types_list["INPUT"], r"input\b", TokenCategory.KEYWORD),
        TokenSpec("FUNCTION", token_types_list["FUNCTION"], r"func\b", TokenCategory.KEYWORD),
        TokenSpec("ENUM", token_types_list["ENUM"], r"enum\b", TokenCategory.KEYWORD),
        TokenSpec("STRUCTURE", token_types_list["STRUCTURE"], r"struct\b", TokenCategory.KEYWORD),
        TokenSpec("LET", token_types_list["LET"], r"let\b", TokenCategory.KEYWORD),
        TokenSpec("ADD", token_types_list["ADD"], r"add\b", TokenCategory.KEYWORD),
        TokenSpec("SUB", token_types_list["SUB"], r"sub\b", TokenCategory.KEYWORD),
        TokenSpec("DIV", token_types_list["DIV"], r"div\b", TokenCategory.KEYWORD),
        TokenSpec("MUL", token_types_list["MUL"], r"mul\b", TokenCategory.KEYWORD),
        TokenSpec("SIN", token_types_list["SIN"], r"sin\b", TokenCategory.KEYWORD),
        TokenSpec("COS", token_types_list["COS"], r"cos\b", TokenCategory.KEYWORD),
        TokenSpec("TAN", token_types_list["TAN"], r"tan\b", TokenCategory.KEYWORD),
        TokenSpec("CTG", token_types_list["CTG"], r"ctg\b", TokenCategory.KEYWORD),
        TokenSpec("ARCSIN", token_types_list["ARCSIN"], r"arc_sin\b", TokenCategory.KEYWORD),
        TokenSpec("ARCCOS", token_types_list["ARCCOS"], r"arc_cos\b", TokenCategory.KEYWORD),
        TokenSpec("ARCTAN", token_types_list["ARCTAN"], r"arc_tan\b", TokenCategory.KEYWORD),
        TokenSpec("ARCCTG", token_types_list["ARCCTG"], r"arc_ctg\b", TokenCategory.KEYWORD),
        TokenSpec("ROOT", token_types_list["ROOT"], r"root\b", TokenCategory.KEYWORD),
        TokenSpec("POWER", token_types_list["POWER"], r"pow\b", TokenCategory.KEYWORD),
        TokenSpec("SQRT", token_types_list["SQRT"], r"sqrt\b", TokenCategory.KEYWORD),
        TokenSpec("FACTORIAL", token_types_list["FACTORIAL"], r"fact\b", TokenCategory.KEYWORD),
        TokenSpec("TETRATION", token_types_list["TETRATION"], r"tetr\b", TokenCategory.KEYWORD),
        TokenSpec("LOGARITHM", token_types_list["LOGARITHM"], r"log\b", TokenCategory.KEYWORD),
        TokenSpec("LOGARITHMTEN", token_types_list["LOGARITHMTEN"], r"log10\b", TokenCategory.KEYWORD),
        TokenSpec("PUSH", token_types_list["PUSH"], r"push\b", TokenCategory.KEYWORD),
        TokenSpec("POP", token_types_list["POP"], r"pop\b", TokenCategory.KEYWORD),
        TokenSpec("LABEL", token_types_list["LABEL"], r"label\b", TokenCategory.KEYWORD),
    ]