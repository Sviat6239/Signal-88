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
    AST_PRINT,
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
    AST_LABEL,
    AST_PRINT,
    AST_PRTLN,
    AST_READ
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

/* Function declarations */

/*
 *   Takes a list of tokens (produced by the lexer) and builds an Abstract Syntax Tree (AST).
 *   The AST represents the hierarchical structure of the program and the order of operations.
 *   Example: "5 + 3" becomes a node of type AST_BINARY_OP with two children nodes (5 and 3).
 */
ASTNode* parse(TokenList* tokens);

ASTNode* parse_statement(TokenList* tokens, int* pos);
ASTNode* parse_expression(TokenList* tokens, int* pos);
void print_ast(ASTNode* node, int indent);

#endif