#include <mpi.h>
#include <stdio.h>

int main (int argc, char **argv) 
{
	int nproc; 
	int yo; /* Mi dirección: 0<=yo<=(nproc-1) */
	int numero = 101;
	int recibido, bandera;
	MPI_Status estado;
	MPI_Request req;

	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &nproc); //Se rescata el Número de procesos
	MPI_Comm_rank(MPI_COMM_WORLD, &yo); //Se rescata el ID del proceso

	printf("Soy el proceso: %d de un total de %d\n", yo, nproc);

	if (yo == 0)
		MPI_Isend(&numero, 1, MPI_INT, 2, 111, MPI_COMM_WORLD, &req);

	if (yo == 2)
	{
		MPI_Irecv(&recibido, 100, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &req);
		do
		{
			//cualquier otro procesamiento ....
			MPI_Test(&req, &bandera, &estado);

		}while(bandera == 0);

		printf("Proceso [%d] :: recibido = %d\n", yo, recibido);
	}

	MPI_Finalize();
	return 0;
}
//Compilar con: mpicc prog.c -O3
//Ejecutar como: mpirun -np 8 ./a.out
