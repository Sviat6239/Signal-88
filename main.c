#include <stdio.h>


int main(){    
    FILE *fptr;

    fptr = fopen("code.bas", "r");

    char String[100];

    if(fptr == NULL){
        printf("Not able to open the file");
    } else {
            while(fgets(String, 100, fptr)){
                printf("%s", String);
            }
    }

    fclose(fptr);
}