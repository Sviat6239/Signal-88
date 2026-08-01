#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include "frontend/include/lexer.h"
#include "frontend/include/parser.h"
#include "frontend/include/utils.h"

int main(int argc, char* argv[]){
    if (argc < 2){
        fprintf(stderr, "Error: No source file specified.\n");
        fprintf(stderr, "Please provide the path to the source code file when running the program.\n");
        fprintf(stderr, "Example usage: %s examples/test.txt\n", argv[0]);
        return EXIT_FAILURE;
    }

    char* source_code = read_file(argv[1]);
    printf("Source code:\n%s\n\n", source_code);

    TokenList tokens = lex(source_code);
    printf("Tokens:\n");
    print_tokens(&tokens);

    ASTNode* ast = parse(&tokens);
    printf("\nAST:\n");
    print_ast(ast, 0);

    free(source_code);
    return 0;
}