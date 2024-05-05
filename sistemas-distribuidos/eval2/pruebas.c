#include <stdio.h>
#include <stdlib.h>

#define DIM 20

void imprimir_vectores(double** vectores, int num_vectores, int k);

int main() {
    int num_vectores, k;
    double vector[DIM];

    // Leer el número de vectores y el tamaño de cada cluster
    scanf("%d", &num_vectores);
    scanf("%d", &k);

    // Almacenar todos los vectores
    double** vectores = (double**)malloc(num_vectores * sizeof(double*));
    for (int i = 0; i < num_vectores; i++) {
        vectores[i] = (double*)malloc(DIM * sizeof(double));
        for (int j = 0; j < DIM; j++) {
            scanf("%lf", &vectores[i][j]);
        }
    }
    imprimir_vectores(vectores, num_vectores, k);
    // Liberar memoria
    for (int i = 0; i < num_vectores; i++) {
        free(vectores[i]);
    }
    free(vectores);

    return 0;
}

void imprimir_vectores(double** vectores, int num_vectores, int k) {
    // Imprimir información relevante
    printf("Cantidad de vectores: %d\n", num_vectores);
    printf("Tamaño de los clusters: %d\n", k);

    // Imprimir vectores
    for (int i = 0; i < num_vectores; i++) {
        for (int j = 0; j < DIM; j++) {
            printf("%.3f ", vectores[i][j]);
        }
        printf("\n");
    }
}