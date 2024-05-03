#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // Verificar que se ingrese el nombre del archivo como argumento
    if (argc != 2) {
        printf("Uso: %s <nombre_del_archivo>\n", argv[0]);
        return 1;
    }

    // Intentar abrir el archivo
    FILE *archivo = fopen(argv[1], "r");
    if (archivo == NULL) {
        perror("Error al abrir el archivo");
        return 1;
    }

    // Leer y mostrar el contenido del archivo línea por línea
    char linea[100]; // Tamaño máximo de una línea, ajusta según necesites
    while (fgets(linea, sizeof(linea), archivo) != NULL) {
        printf("%s", linea);
    }

    // Cerrar el archivo
    fclose(archivo);

    return 0;
}
