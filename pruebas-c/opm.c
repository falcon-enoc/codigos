#include <stdio.h>
#include <omp.h>

int main(){
    #pragma omp parallel
    {
    printf("Hola desde el hilo %d\n", omp_get_thread_num());
    }
    int n = 10;
    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        printf("Procesando el elemento %d por el hilo %d\n", i, omp_get_thread_num());
    }   

    return 0;
}
