#include <stdio.h>
#include <math.h>

// Función supuesta para convertir un char a int
int convcharint(char dato) {
    if (dato >= '0' && dato <= '9') {
        return dato - '0';
    } else if (dato >= 'A' && dato <= 'F') {
        return 10 + (dato - 'A');
    }else {
        return -1; // Error en caso de caracter inválido
    }

int main() {
    int num_digitos;
    printf("Ingrese cantidad de dígitos: ");
    scanf("%d", &num_digitos);

    char digitos[num_digitos];
    for (int i = 0; i < num_digitos; i++) {
        printf("Ingrese dígito %d: ", i + 1);
        scanf(" %c", &digitos[i]);  // Espacio antes de %c para consumir cualquier espacio en blanco
    }

    int numero_base10 = 0;
    for (int i = 0; i < num_digitos; i++) {
        int valor = convcharint(digitos[i]);
        if (valor == -1) {
            printf("Dígito hexadecimal inválido: %c\n", digitos[i]);
            return 1;
        }
        numero_base10 += valor * pow(16, num_digitos - 1 - i);
    }

    printf("El número en base 10 es: %d\n", numero_base10);
    return 0;
}
