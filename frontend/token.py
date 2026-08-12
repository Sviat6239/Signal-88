class TokenType:
    def __init__(self, name: str, reges: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return f"TokenType(name='{self.name}', regex=r'{self.regex}')"

class Token:
    def __init__(self, type: TokenType, value: str, position: int, line: int = 1, column: int = 1, is_nullable: bool = False):
        self.type = type
        self.value = value
        self.position = position
        self.line = line
        self.column = column
        self.is_nullable = is_nullable

    def __repr__(self):
        return f"Token(type={self.type.name}, value='{self.value}', pos={self.position}, line={self.line}, col={self.column}, nullable={self.is_nullable})"


token_types_list = {
    'NUMBER': TokenType("NUMBER", r'-?\d+(\.\d+)?([eE][+-]?\d+)?'),
    'STRING': TokenType("STRING", r'\"[^\"\n]*\"|\'[^\'\n]*\''),
    'CHAR': TokenType("CHAR", r'\'[^\']?\''),  
    'VARIABLE': TokenType("VARIABLE", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b(?!\s*(?:))'),
    'TRUE': TokenType("TRUE", r'\btrue\b'), 
    'FALSE': TokenType("FALSE", r'\bfalse\b'),
    'NULL': TokenType("NULL", r'\bnull\b'),  

    'ASSIGN': TokenType("ASSIGN", r'='),
    'EQUAL': TokenType("EQUAL", r'=='),
    'NOT_EQUAL': TokenType("NOT_EQUAL", r'!='),
    'LESS': TokenType("LESS", r'<'),
    'GREATER': TokenType("GREATER", r'>'),
    'LESS_EQUAL': TokenType("LESS_EQUAL", r'<='),
    'GREATER_EQUAL': TokenType("GREATER_EQUAL", r'>='), 
    'PLUS': TokenType("PLUS", r'\+'),
    'MINUS': TokenType("MINUS", r'-'),
    'MULTIPLY': TokenType("MULTIPLY", r'\*'),
    'DIVIDE': TokenType("DIVIDE", r'/'),

    'SEMICOLON': TokenType("SEMICOLON", r';'),
    'COLON': TokenType("COLON", r':'),
    'COMMA': TokenType("COMMA", r','),
    'DOT': TokenType("DOT", r'\.'),
    'ARROW': TokenType("ARROW", r'->'),

    'LPAREN': TokenType("LPAREN", r'\('),
    'RPAREN': TokenType("RPAREN", r'\)'),
    'LBRACE': TokenType("LBRACE", r'\{'),
    'RBRACE': TokenType("RBRACE", r'\}'),
    'LBRACKET': TokenType("LBRACKET", r'\['),
    'RBRACKET': TokenType("RBRACKET", r'\]'),

    'IF': TokenType("IF", r'\bif\b'),
    'ELSE': TokenType("ELSE", r'\belse\b'),
    'WHILE': TokenType("WHILE", r'\bwhile\b'),
    'FOR': TokenType("FOR", r'\bfor\b'),
    'SWITCH': TokenType("SWITCH", r'\bswitch\b'),
    'CASE': TokenType("CASE", r'\bcase\b'),
    'DEFAULT': TokenType("DEFAULT", r'\bdefault\b'),
    'BREAK': TokenType("BREAK", r'\bbreak\b'),
    'CONTINUE': TokenType("CONTINUE", r'\bcontinue\b'),
    'RETURN': TokenType("RETURN", r'\breturn\b'),
    'CMP': TokenType("CMP", r'\bcmp\b'),
    'JMP': TokenType("JMP", r'\bjmp\b'),
    'JNE': TokenType("JNE", r'\bjne\b'),
    'JE': TokenType("JE", r'\bje\b'),
    'JLE': TokenType("JLE", r'\bjle\b'),
    'JL': TokenType("JL", r'\bjl\b'),
    'JGE': TokenType("JGE", r'\bjge\b'),
    'JG': TokenType("JG", r'\bjg\b'),
    'MOV': TokenType("MOV", r'\bmov\b'),
    'PRINT': TokenType("PRINT", r'\bprint\b'),
    'INPUT': TokenType("INPUT", r'\binput\b'),
    'FUNCTION': TokenType("FUNCTION", r'\bfunc\b'),
    'ENUM': TokenType("ENUM", r'\benum\b'),
    'STRUCTURE': TokenType("STRUCTURE", r'\bstruct\b'),
    'LET': TokenType("LET", r'\blet\b'),
    'ADD': TokenType("ADD", r'\badd\b'),
    'SUB': TokenType("SUB", r'\bsub\b'),
    'DIV': TokenType("DIV", r'\bdiv\b'),
    'MUL': TokenType("MUL", r'\bmul\b'),
    'SIN': TokenType("SIN", r'\bsin\b'),
    'COS': TokenType("COS", r'\bcos\b'),
    'TAN': TokenType("TAN", r'\btan\b'),
    'CTG': TokenType("CTG", r'\bctg\b'),
    'ARCSIN': TokenType("ARCSIN", r'\barc_sin\b'),
    'ARCCOS': TokenType("ARCCOS", r'\barc_cos\b'),
    'ARCTAN': TokenType("ARCTAN", r'\barc_tan\b'),
    'ARCCTG': TokenType("ARCCTG", r'\barc_ctg\b'),
    'ROOT': TokenType("ROOT", r'\broot\b'),
    'POWER': TokenType("POWER", r'\bpow\b'),
    'SQRT': TokenType("SQRT", r'\bsqrt\b'),
    'FACTORIAL': TokenType("FACTORIAL", r'\bfact\b'),
    'TETRATION': TokenType("TETRATION", r'\btetr\b'),
    'LOGARITHM': TokenType("LOGARITHM", r'\blog\b'),
    'LOGARITHMTEN': TokenType("LOGARITHMTEN", r'\blog10\b'),
    'PUSH': TokenType("PUSH", r'\bpush\b'),
    'POP': TokenType("POP", r'\bpop\b'),
    'LABEL': TokenType("LABEL", r'\blabel\b'),

    'MUT': TokenType("MUT", r'\bmut\b'),
    'IMM': TokenType("IMM", r'\bimm\b'),

    'I8': TokenType("I8", r'\bi8\b'),
    'I16': TokenType("I16", r'\bi16\b'),
    'I32': TokenType("I32", r'\bi32\b'),
    'I64': TokenType("I64", r'\bi64\b'),
    'UI8': TokenType("UI8", r'\bui8\b'),
    'UI16': TokenType("UI16", r'\bui16\b'),
    'UI32': TokenType("UI32", r'\bui32\b'),
    'UI64': TokenType("UI64", r'\bui64\b'),
    'F32': TokenType("F32", r'\bf32\b'),
    'F64': TokenType("F64", r'\bf64\b'),
    'CHAR': TokenType("CHAR", r'\bchar\b'),
    'STRING': TokenType("STRING", r'\bstr\b'),
    'LIST': TokenType("LIST", r'\blist\b'),
    'ARRAY': TokenType("ARRAY", r'\barray\b'),
    'BOOL': TokenType("BOOL", r'\bbool\b'),
    'NULL': TokenType("NULL", r'\bnull\b'),
    'VOID': TokenType("VOID", r'\bvoid\b'),

    'MALLOC': TokenType("MALLOC", r'\bmalloc\b'),
    'CALLOC': TokenType("CALLOC", r'\bcalloc\b'),
    'REALLOC': TokenType("REALLOC", r'\brealloc\b'),
    'FREE': TokenType("FREE", r'\bfree\b'),

    'MEMCPY': TokenType("MEMCPY", r'\bmemcpy\b'),
    'MEMMOVE': TokenType("MEMMOVE", r'\bmemmove\b'),
    'MEMSET': TokenType("MEMSET", r'\bmemset\b'),
    'MEMCMP': TokenType("MEMCMP", r'\bmemcmp\b'),
    'SIZEOF': TokenType("SIZEOF", r'\bsizeof\b'),

    'SPACE': TokenType("SPACE", r'[ \n\t\r]+'),
    'COMMENT': TokenType("COMMENT", r'\/\/.*'),  
    'EOF': TokenType("EOF", r''),
}

token_types = {name: token_type for name, token_type in token_types_list.items()}