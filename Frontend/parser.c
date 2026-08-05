#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./include/parser.h"

// Forward declarations for recursive parsing
ASTNode* parse_statement(TokenList* tokens, int* pos);
ASTNode* parse_expression(TokenList* tokens, int* pos);
ASTNode* parse_block(TokenList* tokens, int* pos);
ASTNode* parse_if_statement(TokenList* tokens, int* pos);

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

ASTNode* parse_call_expression(TokenList* tokens, int* pos, char* function_name) {
    ASTNode* call_node = create_node(AST_CALL, 0, function_name, NULL, NULL, 0, NULL, NULL);
    ASTNode* arg_head = NULL;
    ASTNode* arg_current = NULL;

    (*pos)++; // Consume '('

    while (tokens->tokens[*pos].type != TOKEN_RPAREN) {
        ASTNode* arg = parse_expression(tokens, pos);
        if (arg_head == NULL) {
            arg_head = arg;
            arg_current = arg;
        } else {
            arg_current->next = arg;
            arg_current = arg_current->next;
        }

        if (tokens->tokens[*pos].type == TOKEN_COMMA) {
            (*pos)++;
        } else if (tokens->tokens[*pos].type != TOKEN_RPAREN) {
            printf("Syntax error: expected ',' or ')' in argument list at pos=%d\n", *pos);
            exit(1);
        }
    }

    (*pos)++; // Consume ')'
    call_node->left = arg_head;
    return call_node;
}

ASTNode* parse_primary_expression(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];
    ASTNode* node = NULL;

    switch (current.type) {
        case TOKEN_NUMBER:
            node = create_node(AST_NUMBER, current.value, NULL, NULL, "i32", 0, NULL, NULL);
            (*pos)++;
            break;
        case TOKEN_LITERAL:
            node = create_node(AST_STRING, 0, NULL, current.name, "str", 0, NULL, NULL);
            (*pos)++;
            break;
        case TOKEN_IDENTIFIER:
            if (tokens->tokens[*pos + 1].type == TOKEN_LPAREN) {
                char func_name[64];
                strncpy(func_name, current.name, 63);
                (*pos)++;
                node = parse_call_expression(tokens, pos, func_name);
            } else {
                node = create_node(AST_VAR, 0, current.name, NULL, lookup_symbol(current.name), 0, NULL, NULL);
                (*pos)++;
            }
            break;
        case TOKEN_LPAREN:
            (*pos)++;
            node = parse_expression(tokens, pos);
            if (tokens->tokens[*pos].type != TOKEN_RPAREN) {
                printf("Syntax Error: Expected ')' at pos %d\n", *pos);
                exit(1);
            }
            (*pos)++;
            break;
        default:
            printf("Syntax error: unexpected token in expression at pos=%d, type=%d\n", *pos, current.type);
            exit(1);
    }
    return node;
}

ASTNode* parse_expression(TokenList* tokens, int* pos) {
    ASTNode* left = parse_primary_expression(tokens, pos);

    while (tokens->tokens[*pos].type >= TOKEN_GREATER && tokens->tokens[*pos].type <= TOKEN_EQUAL_EQUAL) {
        Token op = tokens->tokens[*pos];
        (*pos)++;
        ASTNode* right = parse_primary_expression(tokens, pos);
        left = create_node(AST_BINARY_OP, op.type, NULL, NULL, NULL, 0, left, right);
    }

    return left;
}

ASTNode* parse_block(TokenList* tokens, int* pos) {
    ASTNode* head = NULL;
    ASTNode* current = NULL;
    (*pos)++; // consume '{'

    while(tokens->tokens[*pos].type != TOKEN_RBRACE && tokens->tokens[*pos].type != TOKEN_EOF) {
        ASTNode* statement = parse_statement(tokens, pos);
        if (head == NULL) {
            head = statement;
            current = head;
        } else {
            current->next = statement;
            current = current->next;
        }
    }

    if (tokens->tokens[*pos].type != TOKEN_RBRACE) {
        printf("Syntax Error: Expected '}' at pos %d\n", *pos);
        exit(1);
    }
    (*pos)++; // consume '}'
    return head;
}

ASTNode* parse_if_statement(TokenList* tokens, int* pos) {
    (*pos)++; // consume 'if'
    
    if (tokens->tokens[*pos].type != TOKEN_LPAREN) {
        printf("Syntax Error: Expected '(' after 'if' at pos %d\n", *pos);
        exit(1);
    }
    (*pos)++; // consume '('

    ASTNode* condition = parse_expression(tokens, pos);

    if (tokens->tokens[*pos].type != TOKEN_RPAREN) {
        printf("Syntax Error: Expected ')' after condition at pos %d\n", *pos);
        exit(1);
    }
    (*pos)++; // consume ')'

    ASTNode* then_block = parse_block(tokens, pos);
    ASTNode* else_block = NULL;

    if (tokens->tokens[*pos].type == TOKEN_ELSE) {
        (*pos)++;
        if (tokens->tokens[*pos].type == TOKEN_IF) {
            else_block = parse_if_statement(tokens, pos);
        } else {
            else_block = parse_block(tokens, pos);
        }
    }
    
    ASTNode* if_node = create_node(AST_IF, 0, NULL, NULL, NULL, 0, condition, then_block);
    if_node->next = else_block; // Not ideal, using next for else. A dedicated field would be better.
    
    //This is a bit of a hack. The `if` node's `right` child is the `then` block.
    //The `else` block (or `else if` chain) is stored in a new `AST_ELSE` node pointed to by the `if` node's `right->next`.
    //A better representation would be a dedicated `else_node` pointer in the `AST_IF` struct.
    if(else_block) {
        ASTNode* else_node_wrapper = create_node(AST_ELSE, 0, NULL, NULL, NULL, 0, else_block, NULL);
        then_block->next = else_node_wrapper;
    }


    return if_node;
}


ASTNode* parse_statement(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];
    ASTNode* node = NULL;

    switch(current.type) {
        case TOKEN_LET:
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

        case TOKEN_PRINT:
        case TOKEN_ADD:
        case TOKEN_SUB:
        case TOKEN_MUL:
        case TOKEN_DIV:
        case TOKEN_TOSTR:
            {
                char func_name[64];
                //This is a bit of a hack to get the function name from the token
                if(current.type == TOKEN_PRINT) strncpy(func_name, "print", 63);
                else if(current.type == TOKEN_ADD) strncpy(func_name, "add", 63);
                else if(current.type == TOKEN_SUB) strncpy(func_name, "sub", 63);
                else if(current.type == TOKEN_MUL) strncpy(func_name, "mul", 63);
                else if(current.type == TOKEN_DIV) strncpy(func_name, "div", 63);
                else if(current.type == TOKEN_TOSTR) strncpy(func_name, "tostr", 63);

                (*pos)++;
                node = parse_call_expression(tokens, pos, func_name);
                if (tokens->tokens[*pos].type != TOKEN_SEMICOLON){
                    printf("Syntax error: expected ';' at pos=%d, found %d\n", *pos, tokens->tokens[*pos].type);
                    exit(1);
                }
                (*pos)++;
                return node;
            }

        case TOKEN_PRTLN:
            (*pos)++;
            if (tokens->tokens[*pos].type != TOKEN_SEMICOLON){
                printf("Syntax error: expected ';' at pos=%d\n", *pos);
                exit(1);
            }
            (*pos)++;
            return create_node(AST_PRTLN, 0, NULL, NULL, NULL, 0, NULL, NULL);
        
        case TOKEN_IF:
            return parse_if_statement(tokens, pos);

        default:
            printf("Syntax error: Unknown statement at pos=%d type=%d name=%s\n", *pos, current.type, current.name);
            exit(1);
    }
    return NULL;
}

ASTNode* parse(TokenList* tokens) {
    int pos = 0;
    ASTNode* head = NULL;
    ASTNode* current = NULL;

    while (tokens->tokens[pos].type != TOKEN_EOF) {
        ASTNode* statement = parse_statement(tokens, &pos);
        if (statement == NULL) {
            continue;
        }
        if (head == NULL) {
            head = statement;
            current = head;
        } else {
            current->next = statement;
            current = current->next;
        }
    }
    return head;
}

void print_ast(ASTNode* node, int indent) {
    if (node == NULL) return;

    for (int i = 0; i < indent; i++) printf("  ");

    switch(node->type) {
        case AST_NUMBER:
            printf("NUMBER(%d)\n", node->value);
            break;
        case AST_STRING:
            printf("STRING(\"%s\")\n", node->literal_value);
            break;
        case AST_VAR:
            printf("VAR(%s)\n", node->name);
            break;
        case AST_ASSIGN:
            printf("ASSIGN(var: %s, type: %s, mutable: %d)\n", node->name, node->data_type, node->mutability);
            print_ast(node->left, indent + 1);
            break;
        case AST_CALL:
            printf("CALL(%s)\n", node->name);
            for (int i = 0; i < indent + 1; i++) printf("  ");
            printf("ARGS:\n");
            print_ast(node->left, indent + 2);
            break;
        case AST_PRINT:
            printf("PRINT\n");
            print_ast(node->left, indent + 1);
            break;
        case AST_PRTLN:
            printf("PRTLN\n");
            break;
        case AST_IF:
            printf("IF\n");
            for (int i = 0; i < indent + 1; i++) printf("  ");
            printf("CONDITION:\n");
            print_ast(node->left, indent + 2);
            for (int i = 0; i < indent + 1; i++) printf("  ");
            printf("THEN:\n");
            print_ast(node->right, indent + 2);
            break;
        case AST_ELSE:
            printf("ELSE\n");
            print_ast(node->left, indent + 1);
            break;
        case AST_BINARY_OP:
            printf("BINARY_OP(%d)\n", node->value);
            print_ast(node->left, indent + 1);
            print_ast(node->right, indent + 1);
            break;
        default:
            printf("UNKNOWN NODE\n");
    }

    print_ast(node->next, indent);
}