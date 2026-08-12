#ifndef LEXER_H
#define LEXER_H

typedef enum{
    TOKEN_NUMBER,
    TOKEN_LITERAL,
    TOKEN_FLOAT,
    TOKEN_LET,
    TOKEN_ADD,
    TOKEN_MUL,
    TOKEN_SUB,
    TOKEN_DIV,
    TOKEN_SQR,
    TOKEN_ROOT,
    TOKEN_SIN,
    TOKEN_COS,
    TOKEN_TAN,
    TOKEN_CTG,
    TOKEN_ARC_SIN,
    TOKEN_ARC_COS,
    TOKEN_ARC_TAN,
    TOKEN_ARC_CTG,
    TOKEN_LOG,
    TOKEN_LOGTEN,
    TOKEN_POW,
    TOKEN_TETR,
    TOKEN_FACT,
    TOKEN_LABEL,
    TOKEN_JMP,
    TOKEN_PRINT,
    TOKEN_PRTLN,
    TOKEN_READ,
    TOKEN_TOSTR,
    TOKEN_TOINT,
    TOKEN_IF,
    TOKEN_ELSE,
    TOKEN_GREATER,
    TOKEN_LESS,
    TOKEN_GREATER_EQUAL,
    TOKEN_LESS_EQUAL,
    TOKEN_NOT_EQUAL,
    TOKEN_EQUAL,
    TOKEN_EQUAL_EQUAL,
    TOKEN_EXCLAMATION,
    TOKEN_QUESTION,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_STAR,
    TOKEN_SLASH,
    TOKEN_BACKSLASH,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_LBRACKET,
    TOKEN_RBRACKET,
    TOKEN_LCURLY,
    TOKEN_RCURLY,
    TOKEN_AMPERSAND,
    TOKEN_PIPE,
    TOKEN_ARROW,
    TOKEN_HASH,
    TOKEN_TILDE,
    TOKEN_PERCENT,
    TOKEN_DOLLAR,
    TOKEN_AT,
    TOKEN_COMMA,
    TOKEN_UNDERSCORE,
    TOKEN_PLUS_EQUAL,
    TOKEN_PLUS_PLUS,
    TOKEN_MINUS_EQUAL,
    TOKEN_MINUS_MINUS,
    TOKEN_SEMICOLON,
    TOKEN_COLON,
    TOKEN_LARROW,
    TOKEN_RARROW,
    TOKEN_EOF,
    TOKEN_MUT,
    TOKEN_IMM,
    TOKEN_I64,
    TOKEN_UI64,
    TOKEN_I32,
    TOKEN_UI32,
    TOKEN_I16,
    TOKEN_UI16,
    TOKEN_I8,
    TOKEN_UI8,
    TOKEN_F64,
    TOKEN_F32,
    TOKEN_STR,
    TOKEN_CHAR,
    TOKEN_FUNC,
    TOKEN_FOR,
    TOKEN_WHILE,
    TOKEN_SWITCH,
    TOKEN_CASE,
    TOKEN_MOV,
    TOKEN_PUSH,
    TOKEN_POP,
    TOKEN_CMP,
    TOKEN_JNE,
    TOKEN_JE,
    TOKEN_JGE,
    TOKEN_JG,
    TOKEN_JLE,
    TOKEN_JL,
    TOKEN_ENUM,
    TOKEN_STRUCT,
    TOKEN_IDENTIFIER
} TokenType;

typedef struct {
    TokenType type;
    int value;
    char name[64];
    const char *data_type;
    int mutability;
} Token;

/*
 * Token list structure
 * Contains an array of tokens and a count
 */
typedef struct {
    Token* tokens;
    int count;
} TokenList;

/* Function declarations */

/*
 *   Takes a string containing source code and converts it into a list of tokens.
 *   Each token represents a meaningful element of the language (number, operator, keyword, identifier, etc.).
 */
TokenList lex(const char* source);

/*
 *   Prints all tokens in a TokenList to the console, for debugging and verification purposes.
 */
void print_tokens(TokenList* list);

#endif