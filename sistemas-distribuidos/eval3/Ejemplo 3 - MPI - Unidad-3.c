#include <mpi.h>
#include <stdio.h>

int main (int argc, char **argv) 
{
	int nproc; 
	int yo; /* Mi dirección: 0<=yo<=(nproc-1) */
	int numero = 101;
	int recibido, bandera=0, fuente, etiqueta, tam=0;
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
		while (bandera == 0)
		{
			//cualquier otro procesamiento ....
			MPI_Iprobe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &bandera, &estado);
		}

		//Rescatando el ID del proceso emisor del mensaje
		fuente = estado.MPI_SOURCE;
		//Rescatando la etiqueta del mensaje que está listo para leerse
		etiqueta = estado.MPI_TAG;
		//Averiguando la longitud del mensaje recibido
		MPI_Get_count(&estado, MPI_INT, &tam);

		//Leyendo el mensaje
		MPI_Irecv(&recibido, tam, MPI_INT, fuente, etiqueta, MPI_COMM_WORLD, &req);

		printf("Proceso [%d] :: fuente = %d :: etiqueta = %d :: tam = %d :: recibido = %d\n", yo, fuente,etiqueta, tam, recibido);
	}

	MPI_Finalize();
	return 0;
}
//Compilar con: mpicc prog.c -O3
//Ejecutar como: mpirun -np 8 ./a.out
