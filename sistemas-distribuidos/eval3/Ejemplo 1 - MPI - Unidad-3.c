#include <mpi.h>
#include <stdio.h>

int main (int argc, char **argv) 
{
	int nproc; 
	int yo; /* Mi dirección: 0<=yo<=(nproc-1) */
	int numero = 101;
	int recibido;
	MPI_Status estado;

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nproc); //Se rescata el Número de procesos
	MPI_Comm_rank(MPI_COMM_WORLD, &yo); //Se rescata el ID del proceso

	printf("Soy el proceso: %d de un total de %d\n", yo, nproc);

	if (yo == 0)
		MPI_Send(&numero, 1, MPI_INT, 2, 111, MPI_COMM_WORLD);

	if (yo == 2)
	{
		MPI_Recv(&recibido, 100, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &estado);
		printf("Proceso [%d] :: recibido = %d\n", yo, recibido);
	}

	MPI_Finalize();
	return 0;
}
//Compilar con: mpicc prog.c -O3
//Ejecutar como: mpirun -np 8 ./a.out
