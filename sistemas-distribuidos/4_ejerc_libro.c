/*
Ejercicio 4

Suponga un vehículo a una velocidad constante de 1.6 km./min.
Haga un programa que exprese la velocidad en km./hora y en m/seg.
*/

#include <stdio.h>

int main(){

    float km_min, km_hora, m_segundos;
    printf("El vehículo va a una velocidad constante de 1.6 km./min.\n");
    km_min = 1.6;
    km_hora = km_min * 60; // Convertir de km/min a km/hora
    m_segundos = km_min * 1000 / 60; // Convertir de km/min a m/segundos
    printf("1.6 km./min. -> %.2f km/h\n", km_hora);
    printf("1.6 km./min. -> %.2f m/s\n", m_segundos);

    return 0;
}

