#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./include/parser.h"

typedef struct {
    char name[64];
    const char* data_type;
} Symbol;

Symbol* symbol_table = NULL;
int symbol_count = 0;
int symbol_capacity = 0;

typedef struct {
    char name[64];
    int target_instruction_index; 
} Label;

Label* label_table = NULL;
int label_count = 0;
int label_capacity = 0;

void init_tables(int initial_capacity) {
    symbol_capacity = initial_capacity;
    symbol_table = (Symbol*)malloc(sizeof(Symbol) * symbol_capacity);
    
    label_capacity = initial_capacity;
    label_table = (Label*)malloc(sizeof(Label) * label_capacity);

    if (symbol_table == NULL || label_table == NULL) {
        printf("Fatal error: Memory allocation failed during initialization!\n");
        exit(1);
    }
}

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

void add_label(const char* name, int position) {
    for (int i = 0; i < label_count; i++) {
        if (strcmp(label_table[i].name, name) == 0) {
            printf("Error: Duplicate label '%s'\n", name);
            exit(1);
        }
    }
    strncpy(label_table[label_count].name, name, 63);
    label_table[label_count].name[63] = '\0';
    label_table[label_count].target_instruction_index = position;
    label_count++;
}

int lookup_label(const char* name) {
    for (int i = 0; i < label_count; i++) {
        if (strcmp(label_table[i].name, name) == 0) {
            return label_table[i].target_instruction_index;
        }
    }
    return -1;
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
            printf("Expected colon at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        const char* d_type = "i32";
        TokenType t_type = tokens->tokens[*pos].type;

        if(t_type >= TOKEN_I64 && t_type <= TOKEN_CHAR){
            d_type = tokens->tokens[*pos].data_type;
            (*pos)++;
        }

        if (tokens->tokens[*pos].type != TOKEN_COLON){
            printf("Expected colon at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        if (tokens->tokens[*pos].type != TOKEN_IDENTIFIER){
            printf("Syntax error: expected identifier at pos=%d\n", *pos);
            exit(1);
        }
        Token var = tokens->tokens[*pos];
        (*pos)++;

        if (tokens->tokens[*pos].type != TOKEN_EQUAL){
            printf("Syntax error: expected '=' at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        add_symbol(var.name, d_type);

        ASTNode* expr = parse_expression(tokens, pos);

        if (tokens->tokens[*pos].type != TOKEN_SEMICOLON){
            printf("Syntax error: expected ';' at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        return create_node(AST_ASSIGN, 0, var.name, NULL, d_type, mutability, expr, NULL);
    }

    else if (current.type == TOKEN_PRINT) {
        (*pos)++;

        if (tokens->tokens[*pos].type != TOKEN_LPAREN) {
            printf("Syntax error: expected '(' at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        ASTNode *expr = parse_expression(tokens, pos); 

        if (tokens->tokens[*pos].type != TOKEN_RPAREN) {
            printf("Syntax error: expected ')' at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        return create_node(AST_PRINT, 0, NULL, NULL, NULL, 0, expr, NULL);
    }

    else if (current.type == TOKEN_PRTLN){
        (*pos)++;

        if (tokens->tokens[*pos].type != TOKEN_SEMICOLON){
            printf("Syntax error: expected ';' at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        return create_node(AST_PRTLN, 0, NULL, NULL, NULL, 0, NULL, NULL);
    }

    else if (current.type == TOKEN_LABEL) {
        Token label_token = tokens->tokens[*pos];
        (*pos)++;

        if (tokens->tokens[*pos].type != TOKEN_COLON) {
            printf("Syntax error: expected ':' after label at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        add_label(label_token.name, current_instruction_index);

        if (tokens->tokens[*pos].type != TOKEN_SEMICOLON){
            printf("Syntax error: expected ';' after label name at pos=%d\n", *pos);
            exit(1);
        }
        (*pos)++;

        return create_node(AST_LABEL, 0, label_token.name, NULL, NULL, 0, NULL, NULL);
    }
}

ASTNode* parse_expression(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];
    ASTNode* left = NULL;
}

void print_ast(ASTNode* node, int indent) {
    if (node == NULL) return;
}