class TokenType:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return f"TokenType(name='{self.name}', regex=r'{self.regex}')"


class Token:
    def __init__(
        self,
        type: TokenType,
        value: str,
        position: int,
        line: int = 1,
        column: int = 1,
        is_nullable: bool = False,
    ):
        self.type = type
        self.value = value
        self.position = position
        self.line = line
        self.column = column
        self.is_nullable = is_nullable

    def __repr__(self):
        return f"Token(type={self.type.name}, value='{self.value}', pos={self.position}, line={self.line}, col={self.column}, nullable={self.is_nullable})"


# Token types definition
token_types_list = {
    # Literals
    "NUMBER": TokenType("NUMBER", r"-?\d+(\.\d+)?([eE][+-]?\d+)?"),  # Numbers (integers, decimals, scientific notation)
    "STRING": TokenType("STRING", r'\"[^\"\n]*\"|\'[^\'\n]*\''),  # String literals
    "CHAR": TokenType("CHAR", r"\'[^\']?\'"),  # Character literals
    "VARIABLE": TokenType("VARIABLE", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b(?!\s*(?:true|false|null|if|else|while|for|switch|case|default|break|continue|return|cmp|jmp|jne|je|jle|jl|jge|jg|mov|print|input|func|enum|struct|let|add|sub|div|mul|sin|cos|tan|ctg|arc_sin|arc_cos|arc_tan|arc_ctg|root|pow|sqrt|fact|tetr|log|log10|push|pop|label|toi8|toi16|toi32|toi64|toui8|toui16|toui32|toui64|tof32|tof64|tostr|tobin|tooct|tohex|mut|imm|i8|i16|i32|i64|ui8|ui16|ui32|ui64|f32|f64|char|str|list|array|bool|void|malloc|calloc|realloc|free|memcpy|memmove|memset|memcmp|sizeof)\b)"),  # Identifiers (excludes keywords)
    "TRUE": TokenType("TRUE", r"\btrue\b"),  # Boolean true
    "FALSE": TokenType("FALSE", r"\bfalse\b"),  # Boolean false
    "NULL": TokenType("NULL", r"\bnull\b"),  # Null literal

    # Operators
    "ASSIGN": TokenType("ASSIGN", r"="),  # Assignment
    "EQUAL": TokenType("EQUAL", r"=="),  # Equality comparison
    "NOT_EQUAL": TokenType("NOT_EQUAL", r"!="),  # Inequality comparison
    "LESS": TokenType("LESS", r"<"),  # Less than
    "GREATER": TokenType("GREATER", r">"),  # Greater than
    "LESS_EQUAL": TokenType("LESS_EQUAL", r"<="),  # Less than or equal
    "GREATER_EQUAL": TokenType("GREATER_EQUAL", r">="),  # Greater than or equal
    "PLUS": TokenType("PLUS", r"\+"),  # Addition
    "MINUS": TokenType("MINUS", r"-"),  # Subtraction
    "MULTIPLY": TokenType("MULTIPLY", r"\*"),  # Multiplication
    "DIVIDE": TokenType("DIVIDE", r"/"),  # Division

    # Delimiters
    "SEMICOLON": TokenType("SEMICOLON", r";"),  # Statement terminator
    "COLON": TokenType("COLON", r":"),  # Type annotation or label separator
    "COMMA": TokenType("COMMA", r","),  # Separator
    "DOT": TokenType("DOT", r"\."),  # Member access
    "ARROW": TokenType("ARROW", r"->"),  # Return type arrow or pointer navigation

    # Brackets
    "LPAREN": TokenType("LPAREN", r"\("),  # Left parenthesis
    "RPAREN": TokenType("RPAREN", r"\)"),  # Right parenthesis
    "LBRACE": TokenType("LBRACE", r"\{"),  # Left brace
    "RBRACE": TokenType("RBRACE", r"\}"),  # Right brace
    "LBRACKET": TokenType("LBRACKET", r"\["),  # Left bracket
    "RBRACKET": TokenType("RBRACKET", r"\]"),  # Right bracket

    # Keywords (Control Flow & Declarations)
    "IF": TokenType("IF", r"\bif\b"),  # Conditional if
    "ELSE": TokenType("ELSE", r"\belse\b"),  # Conditional else
    "WHILE": TokenType("WHILE", r"\bwhile\b"),  # While loop
    "FOR": TokenType("FOR", r"\bfor\b"),  # For loop
    "SWITCH": TokenType("SWITCH", r"\bswitch\b"),  # Switch statement
    "CASE": TokenType("CASE", r"\bcase\b"),  # Switch case branch
    "DEFAULT": TokenType("DEFAULT", r"\bdefault\b"),  # Switch default branch
    "BREAK": TokenType("BREAK", r"\bbreak\b"),  # Loop break statement
    "CONTINUE": TokenType("CONTINUE", r"\bcontinue\b"),  # Loop continue statement
    "RETURN": TokenType("RETURN", r"\breturn\b"),  # Function return
    "CMP": TokenType("CMP", r"\bcmp\b"),  # Compare instruction
    "JMP": TokenType("JMP", r"\bjmp\b"),  # Unconditional jump
    "JNE": TokenType("JNE", r"\bjne\b"),  # Jump if not equal
    "JE": TokenType("JE", r"\bje\b"),  # Jump if equal
    "JLE": TokenType("JLE", r"\bjle\b"),  # Jump if less or equal
    "JL": TokenType("JL", r"\bjl\b"),  # Jump if less
    "JGE": TokenType("JGE", r"\bjge\b"),  # Jump if greater or equal
    "JG": TokenType("JG", r"\bjg\b"),  # Jump if greater
    "JA": TokenType("JA", r"\bja\b"),  # Jump if above
    "JAE": TokenType("JAE", r"\bjae\b"),  # Jump if above or equal
    "JB": TokenType("JB", r"\bjb\b"),  # Jump if below
    "JBE": TokenType("JBE", r"\bjbe\b"),  # Jump if below or equal
    "MOV": TokenType("MOV", r"\bmov\b"),  # Move value
    "PRINT": TokenType("PRINT", r"\bprint\b"),  # Output function
    "INPUT": TokenType("INPUT", r"\binput\b"),  # Input function
    "FUNCTION": TokenType("FUNCTION", r"\bfunc\b"),  # Function declaration
    "ENUM": TokenType("ENUM", r"\benum\b"),  # Enum declaration
    "STRUCTURE": TokenType("STRUCTURE", r"\bstruct\b"),  # Structure declaration
    "LET": TokenType("LET", r"\blet\b"),  # Variable declaration
    "ADD": TokenType("ADD", r"\badd\b"),  # Add instruction
    "SUB": TokenType("SUB", r"\bsub\b"),  # Subtract instruction
    "DIV": TokenType("DIV", r"\bdiv\b"),  # Divide instruction
    "MUL": TokenType("MUL", r"\bmul\b"),  # Multiply instruction
    "SIN": TokenType("SIN", r"\bsin\b"),  # Sine function
    "COS": TokenType("COS", r"\bcos\b"),  # Cosine function
    "TAN": TokenType("TAN", r"\btan\b"),  # Tangent function
    "CTG": TokenType("CTG", r"\bctg\b"),  # Cotangent function
    "ARCSIN": TokenType("ARCSIN", r"\barc_sin\b"),  # Arcsine function
    "ARCCOS": TokenType("ARCCOS", r"\barc_cos\b"),  # Arccosine function
    "ARCTAN": TokenType("ARCTAN", r"\barc_tan\b"),  # Arctangent function
    "ARCCTG": TokenType("ARCCTG", r"\barc_ctg\b"),  # Arccotangent function
    "ROOT": TokenType("ROOT", r"\broot\b"),  # N-th root function
    "POWER": TokenType("POWER", r"\bpow\b"),  # Exponentiation function
    "SQRT": TokenType("SQRT", r"\bsqrt\b"),  # Square root function
    "FACTORIAL": TokenType("FACTORIAL", r"\bfact\b"),  # Factorial function
    "TETRATION": TokenType("TETRATION", r"\btetr\b"),  # Tetration function
    "LOGARITHM": TokenType("LOGARITHM", r"\blog\b"),  # Logarithm function
    "LOGARITHMTEN": TokenType("LOGARITHMTEN", r"\blog10\b"),  # Base-10 logarithm function
    "PUSH": TokenType("PUSH", r"\bpush\b"),  # Push onto stack
    "POP": TokenType("POP", r"\bpop\b"),  # Pop from stack
    "LABEL": TokenType("LABEL", r"\blabel\b"),  # Code label definition
    "IMPORT": TokenType("IMPORT", r"\bimport\b"), #Imports the choised character

    # Type Casts / Conversions
    "TOI8": TokenType("TOI8", r"\btoi8\b"),  # Cast to 8-bit signed integer
    "TOI16": TokenType("TOI16", r"\btoi16\b"),  # Cast to 16-bit signed integer
    "TOI32": TokenType("TOI32", r"\btoi32\b"),  # Cast to 32-bit signed integer
    "TOI64": TokenType("TOI64", r"\btoi64\b"),  # Cast to 64-bit signed integer
    "TOUI8": TokenType("TOUI8", r"\btoui8\b"),  # Cast to 8-bit unsigned integer
    "TOUI16": TokenType("TOUI16", r"\btoui16\b"),  # Cast to 16-bit unsigned integer
    "TOUI32": TokenType("TOUI32", r"\btoui32\b"),  # Cast to 32-bit unsigned integer
    "TOUI64": TokenType("TOUI64", r"\btoui64\b"),  # Cast to 64-bit unsigned integer
    "TOF32": TokenType("TOF32", r"\btof32\b"),  # Cast to 32-bit float
    "TOF64": TokenType("TOF64", r"\btof64\b"),  # Cast to 64-bit float
    "TOSTR": TokenType("TOSTR", r"\btostr\b"),  # Cast to string
    "TOBIN": TokenType("TOBIN", r"\btobin\b"),  # Cast to binary string representation
    "TOOCT": TokenType("TOOCT", r"\btooct\b"),  # Cast to octal string representation
    "TOHEX": TokenType("TOHEX", r"\btohex\b"),  # Cast to hexadecimal string representation

    # Mutability Modifiers
    "MUT": TokenType("MUT", r"\bmut\b"),  # Mutable modifier
    "IMM": TokenType("IMM", r"\bimm\b"),  # Immutable modifier

    # Type Declarations
    "I8": TokenType("I8", r"\bi8\b"),  # 8-bit signed integer type
    "I16": TokenType("I16", r"\bi16\b"),  # 16-bit signed integer type
    "I32": TokenType("I32", r"\bi32\b"),  # 32-bit signed integer type
    "I64": TokenType("I64", r"\bi64\b"),  # 64-bit signed integer type
    "UI8": TokenType("UI8", r"\bui8\b"),  # 8-bit unsigned integer type
    "UI16": TokenType("UI16", r"\bui16\b"),  # 16-bit unsigned integer type
    "UI32": TokenType("UI32", r"\bui32\b"),  # 32-bit unsigned integer type
    "UI64": TokenType("UI64", r"\bui64\b"),  # 64-bit unsigned integer type
    "F32": TokenType("F32", r"\bf32\b"),  # 32-bit float type
    "F64": TokenType("F64", r"\bf64\b"),  # 64-bit float type
    "CHAR": TokenType("CHAR", r"\bchar\b"),  # Character type
    "STRING": TokenType("STRING", r"\bstr\b"),  # String type
    "LIST": TokenType("LIST", r"\blist\b"),  # Dynamic list type
    "ARRAY": TokenType("ARRAY", r"\barray\b"),  # Fixed-size array type
    "BOOL": TokenType("BOOL", r"\bbool\b"),  # Boolean type
    "NULL": TokenType("NULL", r"\bnull\b"),  # Null type
    "VOID": TokenType("VOID", r"\bvoid\b"),  # Void type

    # Memory Management & Low-level Operations
    "MALLOC": TokenType("MALLOC", r"\bmalloc\b"),  # Allocate memory
    "CALLOC": TokenType("CALLOC", r"\bcalloc\b"),  # Allocate and zero-initialize memory
    "REALLOC": TokenType("REALLOC", r"\brealloc\b"),  # Reallocate memory block
    "FREE": TokenType("FREE", r"\bfree\b"),  # Free allocated memory
    "MEMCPY": TokenType("MEMCPY", r"\bmemcpy\b"),  # Memory copy
    "MEMMOVE": TokenType("MEMMOVE", r"\bmemmove\b"),  # Memory move (safe for overlapping memory)
    "MEMSET": TokenType("MEMSET", r"\bmemset\b"),  # Fill memory with constant byte
    "MEMCMP": TokenType("MEMCMP", r"\bmemcmp\b"),  # Compare memory blocks
    "SIZEOF": TokenType("SIZEOF", r"\bsizeof\b"),  # Size of data type or structure in bytes

    # Whitespace and Comments
    "SPACE": TokenType("SPACE", r"[ \n\t\r]+"),  # Whitespace
    "COMMENT": TokenType("COMMENT", r"\/\/.*"),  # C-style single-line comment
    "EOF": TokenType("EOF", r""),  # End of file
}

# Create a lookup dictionary for quick access
token_types = {name: token_type for name, token_type in token_types_list.items()}