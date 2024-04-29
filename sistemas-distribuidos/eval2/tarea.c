//Evaluacion 2
//Jonathan Avila, Enoc Falcon
//Creacion de Clusters

#include <stdio.h>
#include <stdlib.h>

#define T 8

int main() {
    FILE *archivo;
    char linea[100];
    int numero_puntos;
    int tamano_cluster;

    archivo = fopen("test.txt", "r");

    if (archivo == NULL) {
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }

    // Leer las dos primeras líneas del archivo
    for (int i = 0; i < 2; i++) {
        if (fgets(linea, sizeof(linea), archivo) != NULL) {
            if (i == 0) {
                numero_puntos = atoi(linea);
                printf("Número de puntos: %d\n", numero_puntos);
            } else if (i == 1) {
                tamano_cluster = atoi(linea);
                printf("Tamaño del cluster: %d\n", tamano_cluster);
            }
        }
    }

    // Leer y mostrar el resto del archivo
    printf("Resto del archivo:\n");
    while (fgets(linea, sizeof(linea), archivo) != NULL) {
        printf("%s", linea); // Imprimir o almacenar según tus necesidades
    }

    fclose(archivo);
    return 0;
}
