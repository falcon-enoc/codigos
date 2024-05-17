/*
Ejercicio 5 del libro

Escriba un programa al cual se le ingrese una 
temperatura en grados Celcius y haga la conversión 
a grados Farenheit y Kelvin.
oF = (1.8 * oC) + 32 
oK = oC + 273.2
*/

#include <stdio.h>

int main(){

    float temp_c, temp_f, temp_k;
    printf("Ingrese temperatura en grados celcius: ");
    scanf("%f", &temp_c);

    temp_f = (1.8 * temp_c) + 32;
    temp_k = temp_c + 273.2;

    printf("temperatura en grados Farenheit: %.2f\n", temp_f);
    printf("temperatura en grados Kelvin: %.2f\n", temp_k);

    return 0;
}