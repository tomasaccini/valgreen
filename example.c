#include <stdio.h>
#include <stdlib.h>

int main() {

    /* Uninitialized Values */
    int x;
    if(x) x = 3;
   
    /* Invalid Write */
    char* string = malloc(2 * sizeof(char));
    string[2] = 'C';
   
    /* Invalid Read */
    char c = string[5];

    /* Invalid free */
    free(string);
    free(string);

    /* Memory Leak */
    int* array = malloc(100);
    
    return 0;
}
