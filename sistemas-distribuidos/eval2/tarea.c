//Evaluacion 2
//Jonathan Avila, Enoc Falcon
//Creacion de Clusters

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define DIM 20

void imprimir_matriz(float **matriz, int numero_puntos);
void medir_distancias(float **matriz, int numero_puntos);
int parsear_archivo(char *nombre_archivo, float ***matriz, int *numero_puntos, int *tamano_cluster);

int main() {
	char nombre_archivo[] = "test.txt";
	float **matriz;
    int numero_puntos;
    int tamano_cluster;

    if (!parsear_archivo(nombre_archivo, &matriz, &numero_puntos, &tamano_cluster)) {
        return 1;
    }

	imprimir_matriz(matriz, numero_puntos);

	medir_distancias(matriz, numero_puntos); 
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

void medir_distancias(float **matriz, int numero_puntos) {
    float c1[DIM];
    for (int i = 0; i < DIM; i++) {
        c1[i] = matriz[0][i];
    }

    for(int i = 1; i < numero_puntos; i++){
        float sumatoria = 0;
        for(int j = 0; j < DIM; j++){
            sumatoria += pow((c1[j] - matriz[i][j]), 2);
        }
        float distancia = sqrt(sumatoria);
        printf("Distancia del punto 0 al punto %d es: %.3f\n", i, distancia);
    }
}

int parsear_archivo(char *nombre_archivo, float ***matriz, int *numero_puntos, int *tamano_cluster) {
    FILE *archivo;
    char linea[1024];

    archivo = fopen(nombre_archivo, "r");
    if (archivo == NULL) {
        printf("No se pudo abrir el archivo.\n");
        return 0;
    }

    // Obtener las 2 primeras líneas del archivo
    fgets(linea, sizeof(linea), archivo);
    *numero_puntos = atoi(linea);
    fgets(linea, sizeof(linea), archivo);
    *tamano_cluster = atoi(linea);

    // Crear una matriz dinámica para almacenar los puntos
    *matriz = malloc(*numero_puntos * sizeof(float *));
    if (*matriz == NULL) {
        printf("Fallo la asignación de memoria para la matriz.\n");
        fclose(archivo);
        return 0;
    }

    // Leer y almacenar los datos en la matriz
    int indice = 0;
    while (fgets(linea, sizeof(linea), archivo) != NULL && indice < *numero_puntos) {
        (*matriz)[indice] = malloc(DIM * sizeof(float));
        if ((*matriz)[indice] == NULL) {
            printf("Fallo la asignación de memoria para la fila %d.\n", indice);
            // Liberar memoria previamente asignada
            for (int i = 0; i < indice; i++) {
                free((*matriz)[i]);
            }
            free(*matriz);
            fclose(archivo);
            return 0;
        }
        char *token = strtok(linea, " ");
        int j = 0;
        while (token != NULL && j < DIM) {
            (*matriz)[indice][j] = atof(token); // Cambiado a atof para convertir a float
            token = strtok(NULL, " ");
            j++;
        }
        indice++;
    }

    fclose(archivo);
    return 1;
}
