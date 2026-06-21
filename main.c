#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){    
    FILE *fptr;
    char **lines = NULL;
    size_t count = 0;
    char String[500];

    fptr = fopen("code.bas", "r");

    if(fptr == NULL){
        printf("Not able to open the file");
    } else {
            while(fgets(String, sizeof(String), fptr)){
                String[strcspn(String, "\n")] = '\0';

                char **tmp = realloc(lines, (count + 1) * sizeof(char*));
                if (!tmp){
                    printf("Memory error\n");
                    break;
                }

                lines = tmp;

                lines[count] = malloc(strlen(String) + 1);
                strcpy(lines[count], String);

                count++;
            }

            printf("Our code lines:\n");
            for (size_t i = 0; i < count; i++){
                printf("%zu: %s\n", i, lines[i]);
                free(lines[i]);
            }
            free(lines);
    }

    fclose(fptr);

    return 0;
}