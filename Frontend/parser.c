#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./include/parser.h"

typedef struct {
    char name[64];
    const char* data_type;
} Symbol;

Symbol symbol_table[100];
int symbol_count = 0;

void add_symbol(const char* name, const char* data_type) {
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            symbol_table[i].data_type = data_type;
            return;
        }
    }
    strncpy(symbol_table[symbol_count].name, name, 63);
    symbol_table[symbol_count].data_type = data_type;
    symbol_count++;
}

const char* lookup_symbol(const char* name) {
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            return symbol_table[i].data_type;
        }
    }
    return NULL;
}

ASTNode* create_node(ASTNodeType type, int value, const char* name, const char* literal_value, const char* data_type, int mutability, ASTNode* left, ASTNode* right) {
    ASTNode* node = (ASTNode*)malloc(sizeof(ASTNode));
    node->type = type;
    node->value = value;
    node->data_type = data_type;
    node->mutability = mutability;
    
    if (name != NULL) {
        strncpy(node->name, name, 63);
        node->name[63] = '\0';
    } else {
        node->name[0] = '\0';
    }

    if (literal_value != NULL) {
        strncpy(node->literal_value, literal_value, 63);
        node->literal_value[63] = '\0';
    } else {
        node->literal_value[0] = '\0';
    }
    
    node->left = left;
    node->right = right;
    node->next = NULL;
    return node;
}

ASTNode* parse_statement(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];

    if (current.type == TOKEN_LET){
        (*pos)++;

        int mutability = 0;
        if (tokens->tokens[*pos].type == TOKEN_MUT || tokens->tokens[*pos].type == TOKEN_IMM){
            mutability = (tokens->tokens[*pos].type == TOKEN_MUT) ? 1 : 0;
            (*pos)++;
        }

        if (tokens->tokens[*pos].type != TOKEN_COLON){
            printf("Expected colon on %d\n", tokens->tokens[*pos].line);
            (*pos)++;
            return 1;
        } else{
            (*pos)++;
        }

        const char* d_type = "i32";
        TokenType t_type = tokens->tokens[*pos].type;

        if(t_type >= TOKEN_I64 && t_type <= TOKEN_char){
            d_type = tokens->tokens[*pos].data_type;
            (*pos)++;
        }

        if (tokens->tokens[*pos].type != TOKEN_COLON){
            printf("Expected colon on %d\n", tokens->tokens[*pos].line);
            (*pos)++;
            return 1;
        } else{
            (*pos)++;
        }

    }
}

ASTNode* parse_expression(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];
    ASTNode* left = NULL;
}

void print_ast(ASTNode* node, int indent) {
    if (node == NULL) return;
}