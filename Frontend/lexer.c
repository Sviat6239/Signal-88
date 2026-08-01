#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "./include/lexer.h"

Token create_token(TokenType type, int value, const char* name, const char *data_type, int mutability) {
    Token token;
    token.type = type;
    token.value = value;
    token.data_type = data_type;
    token.mutability = mutability;
    if (name) {
        strncpy(token.name, name, sizeof(token.name) - 1);
        token.name[sizeof(token.name) - 1] = '\0';
    } else {
        token.name[0] = '\0';
    }
    return token;
}

TokenList lex(const char* source) {
    TokenList list;
    list.tokens = malloc(128 * sizeof(Token));
    list.count = 0;

    int i = 0;
    while (source[i] != '\0') {
        char c = source[i];

        if (isspace(c)) {
            i++;
            continue;
        }

        if (c == '"') {
            i++;
            char buffer[64];
            int j = 0;
            while (source[i] != '"' && source[i] != '\0' && j < 63) {
                buffer[j++] = source[i++];
            }
            buffer[j] = '\0';

            if (source[i] == '"') {
                i++;
            } else {
                printf("Syntax error: unterminated string literal\n");
                exit(1);
            }

            list.tokens[list.count++] = create_token(TOKEN_STR, 0, buffer, "str", 0);
            continue;
        }

        if (c == '\'') {
            i++;
            if (source[i] == '\0' || source[i] == '\'') {
                printf("Syntax error: empty character literal\n");
                exit(1);
            }
            
            char char_val = source[i++];
            
            if (source[i] == '\'') {
                i++;
            } else {
                printf("Syntax error: unterminated character literal\n");
                exit(1);
            }

            list.tokens[list.count++] = create_token(TOKEN_CHAR, (int)char_val, NULL, "char", 0);
            continue;
        }

        if (isdigit(c)) {
            char num_buffer[64];
            int j = 0;
            
            while (isdigit(source[i]) && j < 63) {
                num_buffer[j++] = source[i++];
            }

            if (source[i] == '.') {
                num_buffer[j++] = source[i++];
                
                if (!isdigit(source[i])) {
                    printf("Syntax error: expected digit after dot\n");
                    exit(1);
                }
                
                while (isdigit(source[i]) && j < 63) {
                    num_buffer[j++] = source[i++];
                }
                num_buffer[j] = '\0';
                
                list.tokens[list.count++] = create_token(TOKEN_F32, 0, num_buffer, "f32", 0);
            } else {
                num_buffer[j] = '\0';
                int value = atoi(num_buffer);
                list.tokens[list.count++] = create_token(TOKEN_INT, value, NULL, "i32", 0);
            }
            continue;
        }

        if (isalpha(c) || c == '_') {
            char buffer[64];
            int j = 0;

            while ((isalnum(source[i]) || source[i] == '_') && j < 63) {
                buffer[j++] = source[i++];
            }
            buffer[j] = '\0';

            if (strcmp(buffer, "let") == 0)
                list.tokens[list.count++] = create_token(TOKEN_LET, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "echo") == 0)
                list.tokens[list.count++] = create_token(TOKEN_ECHO, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "mut") == 0)
                list.tokens[list.count++] = create_token(TOKEN_MUT, 0, NULL, NULL, 1);
            else if (strcmp(buffer, "umut") == 0)
                list.tokens[list.count++] = create_token(TOKEN_UMUT, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "i64") == 0)
                list.tokens[list.count++] = create_token(TOKEN_I64, 0, NULL, "i64", 0);
            else if (strcmp(buffer, "i32") == 0)
                list.tokens[list.count++] = create_token(TOKEN_I32, 0, NULL, "i32", 0);
            else if (strcmp(buffer, "i16") == 0)
                list.tokens[list.count++] = create_token(TOKEN_I16, 0, NULL, "i16", 0);
            else if (strcmp(buffer, "i8") == 0)
                list.tokens[list.count++] = create_token(TOKEN_I8, 0, NULL, "i8", 0);
            else if (strcmp(buffer, "ui64") == 0)
                list.tokens[list.count++] = create_token(TOKEN_UI64, 0, NULL, "ui64", 0);
            else if (strcmp(buffer, "ui32") == 0)
                list.tokens[list.count++] = create_token(TOKEN_UI32, 0, NULL, "ui32", 0);
            else if (strcmp(buffer, "ui16") == 0)
                list.tokens[list.count++] = create_token(TOKEN_UI16, 0, NULL, "ui16", 0);
            else if (strcmp(buffer, "ui8") == 0)
                list.tokens[list.count++] = create_token(TOKEN_UI8, 0, NULL, "ui8", 0);
            else if (strcmp(buffer, "f64") == 0)
                list.tokens[list.count++] = create_token(TOKEN_F64, 0, NULL, "f64", 0);
            else if (strcmp(buffer, "f32") == 0)
                list.tokens[list.count++] = create_token(TOKEN_F32, 0, NULL, "f32", 0);
            else if (strcmp(buffer, "str") == 0)
                list.tokens[list.count++] = create_token(TOKEN_STR, 0, NULL, "str", 0);
            else if (strcmp(buffer, "char") == 0)
                list.tokens[list.count++] = create_token(TOKEN_CHAR, 0, NULL, "char", 0);
            else if (strcmp(buffer, "if") == 0)
                list.tokens[list.count++] = create_token(TOKEN_IF, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "else") == 0)
                list.tokens[list.count++] = create_token(TOKEN_ELSE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "for") == 0)
                list.tokens[list.count++] = create_token(TOKEN_FOR, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "while") == 0)
                list.tokens[list.count++] = create_token(TOKEN_WHILE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "switch") == 0)
                list.tokens[list.count++] = create_token(TOKEN_SWITCH, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "case") == 0)
                list.tokens[list.count++] = create_token(TOKEN_CASE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "func") == 0)
                list.tokens[list.count++] = create_token(TOKEN_FUNC, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "return") == 0)
                list.tokens[list.count++] = create_token(TOKEN_RETURN, 0, NULL, NULL, 0);
            else
                list.tokens[list.count++] = create_token(TOKEN_IDENTIFIER, 0, buffer, NULL, 0);

            continue;
        }

        switch (c) {
            case '+':
                if (source[i + 1] == '='){
                    list.tokens[list.count++] = create_token(TOKEN_PLUS_EQUAL, 0, NULL, NULL, 0);
                } else if (source[i + 1] == '+'){
                    list.tokens[list.count++] = create_token(TOKEN_PLUS_PLUS, 0, NULL, NULL, 0);
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_PLUS, 0, NULL, NULL, 0);
                }
                break;
            case '-':
                if (source[i + 1] == '='){
                    list.tokens[list.count++] = create_token(TOKEN_MINUS_EQUAL, 0, NULL, NULL, 0);
                } else if (source[i + 1] == '-'){
                    list.tokens[list.count++] = create_token(TOKEN_MINUS_MINUS, 0, NULL, NULL, 0);
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_MINUS, 0, NULL, NULL, 0);
                }
                break;
            case '*': list.tokens[list.count++] = create_token(TOKEN_MULT, 0, NULL, NULL, 0); break;
            case '/': list.tokens[list.count++] = create_token(TOKEN_DIV, 0, NULL, NULL, 0); break;
            case ';': list.tokens[list.count++] = create_token(TOKEN_SEMICOLON, 0, NULL, NULL, 0); break;
            case '(': list.tokens[list.count++] = create_token(TOKEN_LPAREN, 0, NULL, NULL, 0); break;
            case ')': list.tokens[list.count++] = create_token(TOKEN_RPAREN, 0, NULL, NULL, 0); break;
            case '{': list.tokens[list.count++] = create_token(TOKEN_LBRACE, 0, NULL, NULL, 0); break;
            case '}': list.tokens[list.count++] = create_token(TOKEN_RBRACE, 0, NULL, NULL, 0); break;
            case '?': list.tokens[list.count++] = create_token(TOKEN_QUESTION, 0, NULL, NULL, 0); break;
            case '>':
                if (source[i + 1] == '=') {
                    list.tokens[list.count++] = create_token(TOKEN_GREATER_EQUAL, 0, NULL, NULL, 0);
                    i++;
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_GREATER, 0, NULL, NULL, 0);
                }
                break;

            case '<':
                if (source[i + 1] == '=') {
                    list.tokens[list.count++] = create_token(TOKEN_LESS_EQUAL, 0, NULL, NULL, 0);
                    i++;
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_LESS, 0, NULL, NULL, 0);
                }
                break;

            case '=':
                if (source[i + 1] == '=') {
                    list.tokens[list.count++] = create_token(TOKEN_EQUAL_EQUAL, 0, NULL, NULL, 0);
                    i++;
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_EQUAL, 0, NULL, NULL, 0);
                }
                break;
            case '!':
                if (source[i + 1] == '=') {
                    list.tokens[list.count++] = create_token(TOKEN_NOT_EQUAL, 0, NULL, NULL, 0);
                    i++;
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_EXCLAMATION, 0, NULL, NULL, 0);
                }
                break;
            case '&': list.tokens[list.count++] = create_token(TOKEN_AMPERSAND, 0, NULL, NULL, 0); break;
            case '|': list.tokens[list.count++] = create_token(TOKEN_PIPE, 0, NULL, NULL, 0); break;
            case '^': list.tokens[list.count++] = create_token(TOKEN_ARROW, 0, NULL, NULL, 0); break;
            case '#': list.tokens[list.count++] = create_token(TOKEN_HASH, 0, NULL, NULL, 0); break;
            case '~': list.tokens[list.count++] = create_token(TOKEN_TILDE, 0, NULL, NULL, 0); break;
            case '%': list.tokens[list.count++] = create_token(TOKEN_PERCENT, 0, NULL, NULL, 0); break;
            case '$': list.tokens[list.count++] = create_token(TOKEN_DOLLAR, 0, NULL, NULL, 0); break;
            case '@': list.tokens[list.count++] = create_token(TOKEN_AT, 0, NULL, NULL, 0); break;
            case ',': list.tokens[list.count++] = create_token(TOKEN_COMMA, 0, NULL, NULL, 0); break;
            case '_': list.tokens[list.count++] = create_token(TOKEN_UNDERSCORE, 0, NULL, NULL, 0); break;
            default:
                printf("Unknown character: %c\n", c);
                exit(1);
        }
        i++;
    }
    list.tokens[list.count++] = create_token(TOKEN_EOF, 0, NULL, NULL, 0);
    return list;
}

void print_tokens(TokenList* list) {
    for (int i = 0; i < list->count; i++) {
        Token t = list->tokens[i];
        switch (t.type) {
            case TOKEN_CHAR: 
                if (t.value != 0) printf("CHAR_LITERAL('%c')\n", (char)t.value);
                else printf("TYPE_CHAR\n"); 
                break;
            case TOKEN_STR: 
                if (t.name[0] != '\0') printf("STR_LITERAL(\"%s\")\n", t.name);
                else printf("TYPE_STR\n"); 
                break;
            case TOKEN_F32: 
                if (t.name[0] != '\0') printf("F32_LITERAL(%s)\n", t.name);
                else printf("TYPE_F32\n");
                break;
            case TOKEN_F64: printf("TYPE_F64\n"); break;
            case TOKEN_DIV: printf("DIV\n"); break;
            case TOKEN_ECHO: printf("ECHO\n"); break;
            case TOKEN_EOF: printf("EOF\n"); break;
            case TOKEN_EQUAL: printf("EQUAL\n"); break;
            case TOKEN_I16: printf("I16\n"); break;
            case TOKEN_I32: printf("I32\n"); break;
            case TOKEN_I64: printf("I64\n"); break;
            case TOKEN_I8: printf("I8\n"); break;
            case TOKEN_IDENTIFIER: printf("IDENT(%s)\n", t.name); break;
            case TOKEN_INT: printf("NUMBER(%d)\n", t.value); break;
            case TOKEN_LET: printf("LET\n"); break;
            case TOKEN_MINUS: printf("MINUS\n"); break;
            case TOKEN_MULT: printf("MULT\n"); break;
            case TOKEN_MUT: printf("MUT\n"); break;
            case TOKEN_PLUS: printf("PLUS\n"); break;
            case TOKEN_SEMICOLON: printf("SEMI\n"); break;
            case TOKEN_UI16: printf("UI16\n"); break;
            case TOKEN_UI32: printf("UI32\n"); break;
            case TOKEN_UI64: printf("UI64\n"); break;
            case TOKEN_UI8: printf("UI8\n"); break;
            case TOKEN_UMUT: printf("UMUT\n"); break;
            case TOKEN_LPAREN: printf("LPAREN\n"); break;
            case TOKEN_RPAREN: printf("RPAREN\n"); break;
            case TOKEN_LBRACE: printf("LBRACE\n"); break;
            case TOKEN_RBRACE: printf("RBRACE\n"); break;
            case TOKEN_GREATER: printf("GREATER\n"); break;
            case TOKEN_GREATER_EQUAL: printf("GREATER_EQUAL\n"); break;
            case TOKEN_LESS: printf("LESS\n"); break;
            case TOKEN_LESS_EQUAL: printf("LESS_EQUAL\n"); break;
            case TOKEN_EQUAL_EQUAL: printf("EQUAL_EQUAL\n"); break;
            case TOKEN_NOT_EQUAL: printf("NOT_EQUAL\n"); break;
            case TOKEN_EXCLAMATION: printf("EXCLAMATION\n"); break;
            case TOKEN_IF: printf("IF\n"); break;
            case TOKEN_ELSE: printf("ELSE\n"); break;
            case TOKEN_QUESTION: printf("QUESTION\n"); break;
            case TOKEN_FUNC: printf("FUNC\n"); break;
            case TOKEN_FOR: printf("FOR\n"); break;
            case TOKEN_WHILE: printf("WHILE\n"); break;
            case TOKEN_SWITCH: printf("SWITCH\n"); break;
            case TOKEN_CASE: printf("CASE\n"); break;
            case TOKEN_AMPERSAND: printf("AMPERSAND\n"); break;
            case TOKEN_PIPE: printf("PIPE\n"); break;
            case TOKEN_ARROW: printf("ARROW\n"); break;
            case TOKEN_TILDE: printf("TILDE\n"); break;
            case TOKEN_PERCENT: printf("PERCENT\n"); break;
            case TOKEN_DOLLAR: printf("DOLLAR\n"); break;
            case TOKEN_AT: printf("AT\n"); break;
            case TOKEN_COMMA: printf("COMMA\n"); break;
            case TOKEN_UNDERSCORE: printf("UNDERSCORE\n"); break;
            case TOKEN_RETURN: printf("RETURN\n"); break;
            default: printf("UNKNOWN\n"); break;
        }
    }
}