#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "frontend/include/lexer.h"
#include "frontend/include/parser.h"
#include "frontend/include/utils.h"

int main(int argc, char* argv[]){
    init_tables(10);
    if (argc < 2){
        fprintf(stderr, "Error: No source file specified.\n");
        return EXIT_FAILURE;
    }

    char* source_code = read_file(argv[1]);
    printf("Source code:\n%s\n\n", source_code);
    fflush(stdout);

    printf("Starting Lexer...\n");
    fflush(stdout);
    
    TokenList tokens = lex(source_code);
    
    printf("Tokens finished. Printing tokens:\n");
    fflush(stdout);
    print_tokens(&tokens);

    printf("\nStarting Parser...\n");
    fflush(stdout);
    
    ASTNode* ast = parse(&tokens);
    
    printf("\nAST Tree:\n");
    fflush(stdout);
    print_ast(ast, 0);

    free(source_code);
    free_tables();
    return 0;
}