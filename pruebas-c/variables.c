#include <stdio.h>
int main(){
    int k;
    printf("variable sin inicialziar, solo reservada: %d\n", k);
    printf("variable sin inicialziar, solo reservada e imprimiendo el valor de memoria, imprimiendo como entero: %d\n", &k);
    printf("variable sin inicialziar, solo reservada e imprimiendo el valor de memoria, imprimiendo como puntero: %p\n", &k);
    k = 1;
    printf("variable inicializada: %d\n", k);

    printf("escribe numero:");
    scanf("%d", &k);
    printf("variable inicializada: %d", k);
    return 0;
}