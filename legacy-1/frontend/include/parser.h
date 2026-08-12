#ifndef PARSER_H
#define PARSER_H

#include "lexer.h"

/*
 * AST node types
 * Represents different elements of the program syntax
 */
typedef enum{
    AST_NUMBER,
    AST_STRING,
    AST_FLOAT,
    AST_CHARACTER,
    AST_BINARY_OP,
    AST_VAR,
    AST_ASSIGN,
    AST_IF,
    AST_ELSE,
    AST_FUNC,
    AST_SWITCH,
    AST_CASE,
    AST_RETURN,
    AST_CALL,
    AST_FOR,
    AST_WHILE,
    AST_ADD,
    AST_SUB,
    AST_MUL,
    AST_DIV,
    AST_SIN,
    AST_COS,
    AST_TAN,
    AST_CTG,
    AST_POW,
    AST_ARC_SIN,
    AST_ARC_COS,
    AST_ARC_TAN,
    AST_ARC_CTG,
    AST_LOG,
    AST_LOGTEN,
    AST_SQR,
    AST_ROOT,
    AST_TETR,
    AST_FACT,
    AST_LABEL,
    AST_PRINT,
    AST_PRTLN,
    AST_READ,
    AST_CMP,
    AST_PUSH,
    AST_POP,
    AST_JMP,
    AST_JNE,
    AST_JE,
    AST_JGE,
    AST_JG,
    AST_JLE,
    AST_JL,
    AST_ENUM,
    AST_STRUC
} ASTNodeType;

typedef struct ASTNode {
    ASTNodeType type;
    int value;
    char name[64];
    char literal_value[128];
    const char* data_type;
    int mutability;
    struct ASTNode* left;
    struct ASTNode* right;
    struct ASTNode* next;
} ASTNode;

/* --- Function declarations --- */

/* Symbol table management */
void init_tables(int initial_capacity);
void free_tables(void);
void add_symbol(const char* name, const char* data_type);
const char* lookup_symbol(const char* name);

/* Parsing entry points and node generators */
ASTNode* parse(TokenList* tokens);
ASTNode* parse_statement(TokenList* tokens, int* pos);
ASTNode* parse_expression(TokenList* tokens, int* pos);
ASTNode* create_node(ASTNodeType type, int value, const char* name, const char* literal_value, const char* data_type, int mutability, ASTNode* left, ASTNode* right);

/* Debugging */
void print_ast(ASTNode* node, int indent);

#endif