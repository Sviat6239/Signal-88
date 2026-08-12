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

void init_tables(int initial_capacity) {
    symbol_capacity = initial_capacity;
    symbol_table = (Symbol*)malloc(sizeof(Symbol) * symbol_capacity);
    if (symbol_table == NULL) {
        printf("Fatal error: Memory allocation failed!\n");
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

    if (symbol_count >= symbol_capacity) {
        symbol_capacity = (symbol_capacity == 0) ? 8 : symbol_capacity * 2;
        Symbol* new_table = (Symbol*)realloc(symbol_table, sizeof(Symbol) * symbol_capacity);
        if (new_table == NULL) {
            printf("Fatal error: Reallocation failed for symbol table!\n");
            exit(1);
        }
        symbol_table = new_table;
    }

    strncpy(symbol_table[symbol_count].name, name, 63);
    symbol_table[symbol_count].name[63] = '\0';
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

void free_tables() {
    free(symbol_table);
    symbol_table = NULL;
    symbol_count = symbol_capacity = 0;
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

void expect_token(TokenList* tokens, int* pos, TokenType expected, const char* err_msg) {
    if (tokens->tokens[*pos].type != expected) {
        printf("Syntax error: %s at pos=%d\n", err_msg, *pos);
        exit(1);
    }
    (*pos)++;
}

ASTNode* parse_let(TokenList* tokens, int* pos) {
    (*pos)++; // пропускаем TOKEN_LET

    int mutability = 0;
    if (tokens->tokens[*pos].type == TOKEN_MUT || tokens->tokens[*pos].type == TOKEN_IMM) {
        mutability = (tokens->tokens[*pos].type == TOKEN_MUT) ? 1 : 0;
        (*pos)++;
    }

    expect_token(tokens, pos, TOKEN_COLON, "expected ':' after mutability modifier");

    char full_type[64] = "";
    if (tokens->tokens[*pos].data_type) {
        strcat(full_type, tokens->tokens[*pos].data_type);
    }
    (*pos)++;

    if (tokens->tokens[*pos].type == TOKEN_LBRACKET) {
        strcat(full_type, "[");
        (*pos)++;
        strcat(full_type, tokens->tokens[*pos].name);
        (*pos)++;
        expect_token(tokens, pos, TOKEN_RBRACKET, "expected ']' in array type definition");
        strcat(full_type, "]");
    }

    expect_token(tokens, pos, TOKEN_COLON, "expected ':' after type definition");

    Token var = tokens->tokens[*pos];
    expect_token(tokens, pos, TOKEN_IDENTIFIER, "expected identifier name");

    // Регистрируем переменную в таблице символов
    add_symbol(var.name, full_type);

    ASTNode* expr = NULL;
    if (tokens->tokens[*pos].type == TOKEN_EQUAL) {
        (*pos)++;
        expr = parse_expression(tokens, pos);
    }

    if (tokens->tokens[*pos].type == TOKEN_SEMICOLON) {
        (*pos)++;
    }

    // Создаем узел через твою родную функцию create_node
    return create_node(AST_ASSIGN, 0, var.name, NULL, full_type, mutability, expr, NULL);
}

ASTNode* parse_expression(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];
    ASTNode* left = NULL;

    if (current.type == TOKEN_NUMBER) {
        left = create_node(AST_NUMBER, current.value, NULL, NULL, "i32", 0, NULL, NULL);
        (*pos)++;
    } 
    else if (current.type == TOKEN_STR) {
        left = create_node(AST_STRING, 0, NULL, current.name, "str", 0, NULL, NULL);
        (*pos)++;
    }
    else if (current.type == TOKEN_CHAR) {
        left = create_node(AST_CHARACTER, current.value, NULL, NULL, "char", 0, NULL, NULL);
        (*pos)++;
    }
    else if (current.type == TOKEN_LET) {
        left = parse_statement(tokens, pos);
    }
    else if (current.type == TOKEN_IDENTIFIER) {
        Token var = current;
        (*pos)++;

        if (tokens->tokens[*pos].type == TOKEN_LPAREN) {
            (*pos)++;
            ASTNode* args_head = NULL;
            ASTNode* args_tail = NULL;

            while (tokens->tokens[*pos].type != TOKEN_RPAREN && tokens->tokens[*pos].type != TOKEN_EOF) {
                ASTNode* arg = parse_expression(tokens, pos);
                
                if (args_head == NULL) {
                    args_head = arg;
                    args_tail = arg;
                } else {
                    args_tail->next = arg;
                    args_tail = arg;
                }

                if (tokens->tokens[*pos].type == TOKEN_COMMA) {
                    (*pos)++;
                }
            }
            expect_token(tokens, pos, TOKEN_RPAREN, "expected ')' after arguments");
            left = create_node(AST_CALL, 0, var.name, NULL, "void", 0, args_head, NULL);
        } else {
            left = create_node(AST_VAR, 0, var.name, NULL, lookup_symbol(var.name), 0, NULL, NULL);
        }
    }
    else if (current.type == TOKEN_LPAREN) {
        (*pos)++;
        left = parse_expression(tokens, pos);
        expect_token(tokens, pos, TOKEN_RPAREN, "expected ')'");
    }
    else {
        printf("Syntax error: unexpected token at pos=%d, type=%d\n", *pos, current.type);
        exit(1);
    }

    current = tokens->tokens[*pos];
    while (current.type == TOKEN_PLUS || current.type == TOKEN_MINUS ||
           current.type == TOKEN_STAR || current.type == TOKEN_DIV ||
           current.type == TOKEN_EQUAL_EQUAL || current.type == TOKEN_PLUS_PLUS) {

        if (current.type == TOKEN_PLUS_PLUS) { 
            (*pos)++;
            left = create_node(AST_BINARY_OP, '+', NULL, NULL, "i32", 0, left, create_node(AST_NUMBER, 1, NULL, NULL, "i32", 0, NULL, NULL));
        } else {
            char op = 0;
            switch (current.type) {
                case TOKEN_PLUS: op = '+'; break;
                case TOKEN_MINUS: op = '-'; break;
                case TOKEN_STAR: op = '*'; break;
                case TOKEN_DIV: op = '/'; break;
                case TOKEN_EQUAL_EQUAL: op = 'E'; break;
                default: op = 0;   break;
            }
            (*pos)++;
            ASTNode* right = parse_expression(tokens, pos);
            left = create_node(AST_BINARY_OP, op, NULL, NULL, "i32", 0, left, right);
        }
        current = tokens->tokens[*pos];
    }

    return left;
}

ASTNode* parse_statement(TokenList* tokens, int* pos) {
    Token current = tokens->tokens[*pos];

    if (current.type == TOKEN_LET) {
        return parse_let(tokens, pos);
    }
    
    else if (current.type == TOKEN_PRINT) {
        (*pos)++;
        expect_token(tokens, pos, TOKEN_LPAREN, "expected '(' after print");
        
        ASTNode* args_head = NULL;
        ASTNode* args_tail = NULL;

        while (tokens->tokens[*pos].type != TOKEN_RPAREN && tokens->tokens[*pos].type != TOKEN_EOF) {
            ASTNode* arg = parse_expression(tokens, pos);
            if (args_head == NULL) {
                args_head = arg;
                args_tail = arg;
            } else {
                args_tail->next = arg;
                args_tail = arg;
            }
            if (tokens->tokens[*pos].type == TOKEN_COMMA) (*pos)++;
        }
        
        expect_token(tokens, pos, TOKEN_RPAREN, "expected ')' after print arguments");
        expect_token(tokens, pos, TOKEN_SEMICOLON, "expected ';' after print");

        return create_node(AST_PRINT, 0, NULL, NULL, NULL, 0, args_head, NULL);
    }

    else if (current.type == TOKEN_ADD || current.type == TOKEN_SUB || 
             current.type == TOKEN_MUL || current.type == TOKEN_DIV) {
        
        ASTNode* node = malloc(sizeof(ASTNode));
        memset(node, 0, sizeof(ASTNode));
        node->type = AST_CALL;
        
        if (current.type == TOKEN_ADD) strcpy(node->name, "add");
        else if (current.type == TOKEN_SUB) strcpy(node->name, "sub");
        else if (current.type == TOKEN_MUL) strcpy(node->name, "mul");
        else if (current.type == TOKEN_DIV) strcpy(node->name, "div");

        (*pos)++;

        if (tokens->tokens[*pos].type == TOKEN_LPAREN) {
            (*pos)++;
        }

        ASTNode* args_head = NULL;
        ASTNode* args_tail = NULL;

        while (tokens->tokens[*pos].type != TOKEN_RPAREN && 
               tokens->tokens[*pos].type != TOKEN_EOF) {
            
            ASTNode* arg = parse_expression(tokens, pos);
            if (arg) {
                if (!args_head) {
                    args_head = arg;
                    args_tail = arg;
                } else {
                    args_tail->next = arg;
                    args_tail = arg;
                }
            }

            if (tokens->tokens[*pos].type == TOKEN_COMMA) {
                (*pos)++;
            }
        }

        if (tokens->tokens[*pos].type == TOKEN_RPAREN) (*pos)++;
        if (tokens->tokens[*pos].type == TOKEN_SEMICOLON) (*pos)++;

        node->left = args_head;
        return node;
    }

    else if (current.type == TOKEN_PRTLN) {
        (*pos)++;
        expect_token(tokens, pos, TOKEN_SEMICOLON, "expected ';' after prtln");
        return create_node(AST_PRTLN, 0, NULL, NULL, NULL, 0, NULL, NULL);
    }

    else if (current.type == TOKEN_LABEL) {
        (*pos)++;
        expect_token(tokens, pos, TOKEN_COLON, "expected ':' after label keyword");
        
        Token label_var = tokens->tokens[*pos];
        expect_token(tokens, pos, TOKEN_IDENTIFIER, "expected label name");
        expect_token(tokens, pos, TOKEN_SEMICOLON, "expected ';' after label name");

        return create_node(AST_LABEL, 0, label_var.name, NULL, NULL, 0, NULL, NULL);
    }

    else if (current.type == TOKEN_JMP) {
        (*pos)++;
        expect_token(tokens, pos, TOKEN_LPAREN, "expected '(' after jmp");
        
        Token target = tokens->tokens[*pos];
        expect_token(tokens, pos, TOKEN_IDENTIFIER, "expected label identifier inside jmp(...)");
        
        expect_token(tokens, pos, TOKEN_RPAREN, "expected ')' after label target");
        expect_token(tokens, pos, TOKEN_SEMICOLON, "expected ';' after jmp statement");

        return create_node(AST_JMP, 0, target.name, NULL, NULL, 0, NULL, NULL);
    }

    else if (current.type == TOKEN_IF) {
        (*pos)++;
        expect_token(tokens, pos, TOKEN_LPAREN, "expected '(' after if");
        ASTNode* cond = parse_expression(tokens, pos);
        expect_token(tokens, pos, TOKEN_RPAREN, "expected ')' after condition");

        expect_token(tokens, pos, TOKEN_LBRACE, "expected '{' before if body");

        ASTNode* then_body = NULL;
        ASTNode* body_tail = NULL;

        while (tokens->tokens[*pos].type != TOKEN_RBRACE && tokens->tokens[*pos].type != TOKEN_EOF) {
            ASTNode* stmt = parse_statement(tokens, pos);
            if (then_body == NULL) {
                then_body = stmt;
                body_tail = stmt;
            } else {
                body_tail->next = stmt;
                body_tail = stmt;
            }
        }
        expect_token(tokens, pos, TOKEN_RBRACE, "expected '}' after if body");

        ASTNode* else_body = NULL;
        if (tokens->tokens[*pos].type == TOKEN_ELSE) {
            (*pos)++;
            if (tokens->tokens[*pos].type == TOKEN_IF) {
                else_body = parse_statement(tokens, pos);
            } else {
                expect_token(tokens, pos, TOKEN_LBRACE, "expected '{' before else body");
                
                ASTNode* else_tail = NULL;
                while (tokens->tokens[*pos].type != TOKEN_RBRACE && tokens->tokens[*pos].type != TOKEN_EOF) {
                    ASTNode* stmt = parse_statement(tokens, pos);
                    if (else_body == NULL) {
                        else_body = stmt;
                        else_tail = stmt;
                    } else {
                        else_tail->next = stmt;
                        else_tail = stmt;
                    }
                }
                expect_token(tokens, pos, TOKEN_RBRACE, "expected '}' after else body");
            }
        }

        ASTNode* branch_node = create_node(AST_ELSE, 0, NULL, NULL, NULL, 0, then_body, else_body);
        return create_node(AST_IF, 0, NULL, NULL, NULL, 0, cond, branch_node);
    }

    else {
        ASTNode* expr = parse_expression(tokens, pos);
        if (tokens->tokens[*pos].type == TOKEN_SEMICOLON) {
            (*pos)++;
        }
        return expr;
    }
}

ASTNode* parse(TokenList* tokens) {
    int pos = 0;
    ASTNode* head = NULL;
    ASTNode* tail = NULL;

    while (tokens->tokens[pos].type != TOKEN_EOF) {
        ASTNode* stmt = parse_statement(tokens, &pos);
        
        if (stmt != NULL) {
            if (head == NULL) {
                head = stmt;
                tail = stmt;
            } else {
                tail->next = stmt;
                tail = stmt;
            }
        }
    }

    return head;
}

void print_ast(ASTNode* node, int indent) {
    if (node == NULL) return;

    for (int i = 0; i < indent; i++) printf("  ");

    switch (node->type) {
        case AST_NUMBER:
            printf("AST_NUMBER(%d, type: %s)\n", node->value, node->data_type ? node->data_type : "i32");
            break;

        case AST_STRING:
            printf("AST_STRING(\"%s\")\n", node->literal_value[0] != '\0' ? node->literal_value : node->name);
            break;

        case AST_CHARACTER:
            printf("AST_CHARACTER('%c', value: %d)\n", (char)node->value, node->value);
            break;

        case AST_VAR:
            printf("AST_VAR(name: %s, type: %s)\n", node->name, node->data_type ? node->data_type : "unknown");
            break;

        case AST_ASSIGN:
            printf("AST_ASSIGN(var: %s, type: %s, mut: %d)\n", 
                   node->name, 
                   node->data_type ? node->data_type : "reassign", 
                   node->mutability);
            if (node->left) print_ast(node->left, indent + 1);
            break;

        case AST_BINARY_OP:
            if (node->value == 'E') {
                printf("AST_BINARY_OP(==)\n");
            } else {
                printf("AST_BINARY_OP(%c)\n", node->value);
            }
            if (node->left) print_ast(node->left, indent + 1);
            if (node->right) print_ast(node->right, indent + 1);
            break;

        case AST_PRINT:
            printf("AST_PRINT\n");
            for (ASTNode* arg = node->left; arg != NULL; arg = arg->next) {
                print_ast(arg, indent + 1);
            }
            break;

        case AST_PRTLN:
            printf("AST_PRTLN\n");
            break;

        case AST_LABEL:
            printf("AST_LABEL(name: %s)\n", node->name);
            break;

        case AST_JMP:
            printf("AST_JMP(target: %s)\n", node->name);
            break;

        case AST_IF:
            printf("AST_IF\n");
            for (int i = 0; i < indent + 1; i++) printf("  ");
            printf("Condition:\n");
            print_ast(node->left, indent + 2);
            
            if (node->right) {
                print_ast(node->right, indent + 1);
            }
            break;

        case AST_ELSE:
            printf("AST_BRANCH (then/else)\n");
            if (node->left) {
                for (int i = 0; i < indent + 1; i++) printf("  ");
                printf("Then Body:\n");
                for (ASTNode* stmt = node->left; stmt != NULL; stmt = stmt->next) {
                    print_ast(stmt, indent + 2);
                }
            }
            if (node->right) {
                for (int i = 0; i < indent + 1; i++) printf("  ");
                printf("Else Body:\n");
                if (node->right->type == AST_IF) {
                    print_ast(node->right, indent + 2);
                } else {
                    for (ASTNode* stmt = node->right; stmt != NULL; stmt = stmt->next) {
                        print_ast(stmt, indent + 2);
                    }
                }
            }
            break;

        case AST_CALL:
            printf("AST_CALL(func: %s)\n", node->name);
            for (ASTNode* arg = node->left; arg != NULL; arg = arg->next) {
                print_ast(arg, indent + 1);
            }
            break;

        case AST_FUNC:
            printf("AST_FUNC(name: %s, return_type: %s)\n", node->name, node->data_type ? node->data_type : "void");
            
            if (node->left != NULL) {
                for (int i = 0; i < indent + 1; i++) printf("  ");
                printf("Params:\n");
                for (ASTNode* p = node->left; p != NULL; p = p->next) {
                    print_ast(p, indent + 2);
                }
            }

            if (node->right != NULL) {
                for (int i = 0; i < indent + 1; i++) printf("  ");
                printf("Body:\n");
                for (ASTNode* stmt = node->right; stmt != NULL; stmt = stmt->next) {
                    print_ast(stmt, indent + 2);
                }
            }
            break;

        case AST_RETURN:
            printf("AST_RETURN\n");
            if (node->left) print_ast(node->left, indent + 1);
            break;

        default:
            printf("AST_NODE(type: %d, name: '%s')\n", node->type, node->name);
            if (node->left) print_ast(node->left, indent + 1);
            if (node->right) print_ast(node->right, indent + 1);
            break;
    }

    if (node->type != AST_VAR && node->next != NULL) {
        print_ast(node->next, indent);
    }
}