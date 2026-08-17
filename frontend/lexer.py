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