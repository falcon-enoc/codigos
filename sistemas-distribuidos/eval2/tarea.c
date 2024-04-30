//Evaluacion 2
//Jonathan Avila, Enoc Falcon
//Creacion de Clusters

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DIM 20

void imprimir_matriz(float **matriz, int numero_puntos);

int main() {
    FILE *archivo;
    char linea[1024];
    int numero_puntos;
    int tamano_cluster;

    archivo = fopen("test.txt", "r");

    if (archivo == NULL) { //comprobaciones apertura de archivo
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }

	// Obtener las 2 primeras lineas del archivo
	fgets(linea, sizeof(linea), archivo);
    numero_puntos = atoi(linea);
    fgets(linea, sizeof(linea), archivo);
    tamano_cluster = atoi(linea);

	// Crear una matriz dinámica para almacenar los puntos
    float **matriz = malloc(numero_puntos * sizeof(float *));
    for (int i = 0; i < numero_puntos; i++) {
        matriz[i] = malloc(DIM * sizeof(float));
        if (matriz[i] == NULL) {
            printf("Fallo la asignación de memoria para la fila %d.\n", i);
            // Liberar memoria previamente asignada
            for (int j = 0; j < i; j++) {
                free(matriz[j]);
            }
            free(matriz);
            fclose(archivo);
            return 1;
        }
    }
	    // Leer y almacenar los datos en la matriz
    int indice = 0;
    while (fgets(linea, sizeof(linea), archivo) != NULL && indice < numero_puntos) {
        char *token = strtok(linea, " ");
        int j = 0;
        while (token != NULL && j < DIM) {
            matriz[indice][j] = atof(token); // Cambiado a atof para convertir a float
            token = strtok(NULL, " ");
            j++;
        }
        indice++;
    }

    fclose(archivo);

	imprimir_matriz(matriz, numero_puntos);

    // Liberar la memoria de la matriz
    for (int i = 0; i < numero_puntos; i++) {
        free(matriz[i]);
    }
    free(matriz);

    return 0;
}

void imprimir_matriz(float **matriz, int numero_puntos) {
    for (int i = 0; i < numero_puntos; i++) {
        for (int j = 0; j < DIM; j++) {
            printf("%.3f ", matriz[i][j]);
        }
        printf("\n");
    }
}