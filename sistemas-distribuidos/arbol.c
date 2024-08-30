#include <stdio.h>

int main() {
    int tam;
    printf("Ingrese el tamaño del arbol: ");
    scanf("%d", &tam);

    for (int i = 1; i <= tam; i++) { 
        for (int j = 0; j < i; j++) {
            printf("*");
        }
        printf("\n");
    }

    printf("======================");
    printf("\n");
    printf("======================");
    printf("\n");


    for (int i = tam; i > 0; i--) { 
        for (int j = i; j > 0; j--) {
            printf("*");
        }
        printf("\n");
    }
    
    
    return 0;
}
