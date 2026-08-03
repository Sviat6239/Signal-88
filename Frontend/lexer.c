#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "./include/lexer.h"

static int is_keyword_boundary(char ch) {
    return ch == '\0' || !(isalnum((unsigned char)ch) || ch == '_' || ch == '-');
}

static int match_keyword(const char* source, int index, const char* keyword) {
    size_t keyword_length = strlen(keyword);

    if (strncmp(source + index, keyword, keyword_length) != 0) {
        return 0;
    }

    return is_keyword_boundary(source[index + keyword_length]);
}

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

            list.tokens[list.count++] = create_token(TOKEN_LITERAL, 0, buffer, "str", 0);
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
                
                list.tokens[list.count++] = create_token(TOKEN_FLOAT, 0, num_buffer, "f32", 0);
            } else {
                num_buffer[j] = '\0';
                int value = atoi(num_buffer);
                list.tokens[list.count++] = create_token(TOKEN_NUMBER, value, NULL, "i32", 0);
            }
            continue;
        }

        if (isalpha(c) || c == '_') {
            if (match_keyword(source, i, "arc-sin")) {
                list.tokens[list.count++] = create_token(TOKEN_ARC_SIN, 0, NULL, NULL, 0);
                i += (int)strlen("arc-sin");
                continue;
            }
            if (match_keyword(source, i, "arc-cos")) {
                list.tokens[list.count++] = create_token(TOKEN_ARC_COS, 0, NULL, NULL, 0);
                i += (int)strlen("arc-cos");
                continue;
            }
            if (match_keyword(source, i, "arc-tan")) {
                list.tokens[list.count++] = create_token(TOKEN_ARC_TAN, 0, NULL, NULL, 0);
                i += (int)strlen("arc-tan");
                continue;
            }
            if (match_keyword(source, i, "arc-tg")) {
                list.tokens[list.count++] = create_token(TOKEN_ARC_TAN, 0, NULL, NULL, 0);
                i += (int)strlen("arc-tg");
                continue;
            }
            if (match_keyword(source, i, "arc-ctg")) {
                list.tokens[list.count++] = create_token(TOKEN_ARC_CTG, 0, NULL, NULL, 0);
                i += (int)strlen("arc-ctg");
                continue;
            }

            char buffer[64];
            int j = 0;

            while ((isalnum(source[i]) || source[i] == '_') && j < 63) {
                buffer[j++] = source[i++];
            }
            buffer[j] = '\0';

            if (strcmp(buffer, "let") == 0)
                list.tokens[list.count++] = create_token(TOKEN_LET, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "add") == 0)
                list.tokens[list.count++] = create_token(TOKEN_ADD, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "sub") == 0)
                list.tokens[list.count++] = create_token(TOKEN_SUB, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "mul") == 0)
                list.tokens[list.count++] = create_token(TOKEN_MUL, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "div") == 0)
                list.tokens[list.count++] = create_token(TOKEN_DIV, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "sqr") == 0)
                list.tokens[list.count++] = create_token(TOKEN_SQR, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "root") == 0)
                list.tokens[list.count++] = create_token(TOKEN_ROOT, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "sin") == 0)
                list.tokens[list.count++] = create_token(TOKEN_SIN, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "cos") == 0)
                list.tokens[list.count++] = create_token(TOKEN_COS, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "tan") == 0)
                list.tokens[list.count++] = create_token(TOKEN_TAN, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "ctg") == 0)
                list.tokens[list.count++] = create_token(TOKEN_CTG, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "log") == 0)
                list.tokens[list.count++] = create_token(TOKEN_LOG, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "log10") == 0 || strcmp(buffer, "logten") == 0)
                list.tokens[list.count++] = create_token(TOKEN_LOGTEN, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "pow") == 0)
                list.tokens[list.count++] = create_token(TOKEN_POW, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "label") == 0)
                list.tokens[list.count++] = create_token(TOKEN_LABEL, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "jmp") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JMP, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "print") == 0)
                list.tokens[list.count++] = create_token(TOKEN_PRINT, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "prtln") == 0)
                list.tokens[list.count++] = create_token(TOKEN_PRTLN, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "read") == 0)
                list.tokens[list.count++] = create_token(TOKEN_READ, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "tostr") == 0)
                list.tokens[list.count++] = create_token(TOKEN_TOSTR, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "toint") == 0)
                list.tokens[list.count++] = create_token(TOKEN_TOINT, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "mut") == 0)
                list.tokens[list.count++] = create_token(TOKEN_MUT, 0, NULL, NULL, 1);
            else if (strcmp(buffer, "imm") == 0)
                list.tokens[list.count++] = create_token(TOKEN_IMM, 0, NULL, NULL, 0);
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
            else if (strcmp(buffer, "mov") == 0)
                list.tokens[list.count++] = create_token(TOKEN_MOV, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "push") == 0)
                list.tokens[list.count++] = create_token(TOKEN_PUSH, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "pop") == 0)
                list.tokens[list.count++] = create_token(TOKEN_POP, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "cmp") == 0)
                list.tokens[list.count++] = create_token(TOKEN_CMP, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "jne") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JNE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "je") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "JGE") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JGE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "jg") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JG, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "jle") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JLE, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "jl") == 0)
                list.tokens[list.count++] = create_token(TOKEN_JL, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "enum") == 0)
                list.tokens[list.count++] = create_token(TOKEN_ENUM, 0, NULL, NULL, 0);
            else if (strcmp(buffer, "struct") == 0)
                list.tokens[list.count++] = create_token(TOKEN_SRUCT, 0, NULL, NULL, 0);
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
                } else if (source[i + 1] == '>') {
                    list.tokens[list.count++] = create_token(TOKEN_RARROW, 0, NULL, NULL, 0);
                    i++;
                } else {
                    list.tokens[list.count++] = create_token(TOKEN_MINUS, 0, NULL, NULL, 0);
                }
                break;
            case '*': list.tokens[list.count++] = create_token(TOKEN_STAR, 0, NULL, NULL, 0); break;
            case '/': list.tokens[list.count++] = create_token(TOKEN_SLASH, 0, NULL, NULL, 0); break;
            case '\\': list.tokens[list.count++] = create_token(TOKEN_BACKSLASH, 0, NULL, NULL, 0); break;
            case ';': list.tokens[list.count++] = create_token(TOKEN_SEMICOLON, 0, NULL, NULL, 0); break;
            case ':': list.tokens[list.count++] = create_token(TOKEN_COLON, 0, NULL, NULL, 0); break;
            case '(': list.tokens[list.count++] = create_token(TOKEN_LPAREN, 0, NULL, NULL, 0); break;
            case ')': list.tokens[list.count++] = create_token(TOKEN_RPAREN, 0, NULL, NULL, 0); break;
            case '[': list.tokens[list.count++] = create_token(TOKEN_LCURLY, 0, NULL, NULL, 0); break;
            case ']': list.tokens[list.count++] = create_token(TOKEN_RCURLY, 0, NULL, NULL, 0); break;
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
                } else if (source[i + 1] == '-') {
                    list.tokens[list.count++] = create_token(TOKEN_LARROW, 0, NULL, NULL, 0);
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
            case TOKEN_LITERAL:
                printf("LITERAL(\"%s\")\n", t.name);
                break;
            case TOKEN_CHAR: 
                if (t.value != 0) printf("CHAR_LITERAL('%c')\n", (char)t.value);
                else printf("TYPE_CHAR\n"); 
                break;
            case TOKEN_FLOAT: 
                if (t.name[0] != '\0') printf("F32_LITERAL(%s)\n", t.name);
                else printf("TYPE_F32\n");
                break;
            case TOKEN_NUMBER: printf("NUMBER(%d)\n", t.value); break;
            case TOKEN_ADD: printf("ADD\n"); break;
            case TOKEN_SUB: printf("SUB\n"); break;
            case TOKEN_MUL: printf("MUL\n"); break;
            case TOKEN_F64: printf("TYPE_F64\n"); break;
            case TOKEN_DIV: printf("DIV\n"); break;
            case TOKEN_SQR: printf("SQR\n"); break;
            case TOKEN_ROOT: printf("ROOT\n"); break;
            case TOKEN_SIN: printf("SIN\n"); break;
            case TOKEN_COS: printf("COS\n"); break;
            case TOKEN_TAN: printf("TAN\n"); break;
            case TOKEN_CTG: printf("CTG\n"); break;
            case TOKEN_ARC_SIN: printf("ARC_SIN\n"); break;
            case TOKEN_ARC_COS: printf("ARC_COS\n"); break;
            case TOKEN_ARC_TAN: printf("ARC_TAN\n"); break;
            case TOKEN_ARC_CTG: printf("ARC_CTG\n"); break;
            case TOKEN_LOG: printf("LOG\n"); break;
            case TOKEN_LOGTEN: printf("LOGTEN\n"); break;
            case TOKEN_POW: printf("POW\n"); break;
            case TOKEN_LABEL: printf("LABEL\n"); break;
            case TOKEN_JMP: printf("JMP\n"); break;
            case TOKEN_PRINT: printf("PRINT\n"); break;
            case TOKEN_PRTLN: printf("PRTLN\n"); break;
            case TOKEN_READ: printf("READ\n"); break;
            case TOKEN_TOSTR: printf("TOSTR\n"); break;
            case TOKEN_TOINT: printf("TOINT\n"); break;
            case TOKEN_THEN: printf("THEN\n"); break;
            case TOKEN_ELSEIF: printf("ELSEIF\n"); break;
            case TOKEN_EOF: printf("EOF\n"); break;
            case TOKEN_EQUAL: printf("EQUAL\n"); break;
            case TOKEN_EQUAL_EQUAL: printf("EQUAL_EQUAL\n"); break;
            case TOKEN_I16: printf("I16\n"); break;
            case TOKEN_I32: printf("I32\n"); break;
            case TOKEN_I64: printf("I64\n"); break;
            case TOKEN_I8: printf("I8\n"); break;
            case TOKEN_IDENTIFIER: printf("IDENT(%s)\n", t.name); break;
            case TOKEN_LET: printf("LET\n"); break;
            case TOKEN_MINUS: printf("MINUS\n"); break;
            case TOKEN_MINUS_EQUAL: printf("MINUS_EQUAL\n"); break;
            case TOKEN_MINUS_MINUS: printf("MINUS_MINUS\n"); break;
            case TOKEN_MUT: printf("MUT\n"); break;
            case TOKEN_PLUS: printf("PLUS\n"); break;
            case TOKEN_PLUS_EQUAL: printf("PLUS_EQUAL\n"); break;
            case TOKEN_PLUS_PLUS: printf("PLUS_PLUS\n"); break;
            case TOKEN_SEMICOLON: printf("SEMI\n"); break;
            case TOKEN_COLON: printf("COLON\n"); break;
            case TOKEN_STAR: printf("STAR\n"); break;
            case TOKEN_SLASH: printf("SLASH\n"); break;
            case TOKEN_BACKSLASH: printf("BACKSLASH\n"); break;
            case TOKEN_UI16: printf("UI16\n"); break;
            case TOKEN_UI32: printf("UI32\n"); break;
            case TOKEN_UI64: printf("UI64\n"); break;
            case TOKEN_UI8: printf("UI8\n"); break;
            case TOKEN_IMM: printf("IMMUT\n"); break;
            case TOKEN_LPAREN: printf("LPAREN\n"); break;
            case TOKEN_RPAREN: printf("RPAREN\n"); break;
            case TOKEN_LBRACE: printf("LBRACE\n"); break;
            case TOKEN_RBRACE: printf("RBRACE\n"); break;
            case TOKEN_LCURLY: printf("LCURLY\n"); break;
            case TOKEN_RCURLY: printf("RCURLY\n"); break;
            case TOKEN_GREATER: printf("GREATER\n"); break;
            case TOKEN_GREATER_EQUAL: printf("GREATER_EQUAL\n"); break;
            case TOKEN_LESS: printf("LESS\n"); break;
            case TOKEN_LESS_EQUAL: printf("LESS_EQUAL\n"); break;
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
            case TOKEN_LARROW: printf("LARROW\n"); break;
            case TOKEN_RARROW: printf("RARROW\n"); break;
            case TOKEN_TILDE: printf("TILDE\n"); break;
            case TOKEN_PERCENT: printf("PERCENT\n"); break;
            case TOKEN_DOLLAR: printf("DOLLAR\n"); break;
            case TOKEN_AT: printf("AT\n"); break;
            case TOKEN_COMMA: printf("COMMA\n"); break;
            case TOKEN_UNDERSCORE: printf("UNDERSCORE\n"); break;
            case TOKEN_STR: printf("TYPE_STR\n"); break;
            case TOKEN_MOV: printf("MOV\n"); break;
            case TOKEN_PUSH: printf("PUSH\n"); break;
            case TOKEN_POP: printf("POP\n"); break;
            case TOKEN_CMP: printf("CMP\n"); break;
            case TOKEN_JNE: printf("JNE\n"); break;
            case TOKEN_JE: printf("JE\n"); break;
            case TOKEN_JGE: printf("JGE\n"); break;
            case TOKEN_JG: printf("JG\n"); break;
            case TOKEN_JLE: printf("JLE\n"); break;
            case TOKEN_JL: printf("JL\n"); break;
            case TOKEN_ENUM: printf("ENUM\n"); break;
            case TOKEN_STRUCT: printf("STRUCT\n"); break;
            default: printf("UNKNOWN\n"); break;
        }
    }
}