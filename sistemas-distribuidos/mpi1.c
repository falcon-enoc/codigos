#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv){

    int nproc;
    int yo;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nproc); 
    MPI_Comm_rank(MPI_COMM_WORLD, &yo);

    printf("Soy el proceso: %d de un total de %d\n", yo, nproc);
    // compilado con:
    // mpicc nombre.c -o nombre
    // correr programa:
    // mpirun -np (numero de nodos) (8) nombre
    MPI_Finalize();
}