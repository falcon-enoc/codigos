//Tarea 1
//Jonathan Avila, Enoc Falcon
#include <stdio.h>
#include <omp.h>

#define N 1000
#define T 8

int main(){
	int arreglo[N];
	int constante = 12;
	//llenado del array
	for (int i=0; i<N;i++){
		arreglo[i]=i+1;
	//	printf("%d, ", arreglo[i]);	
	}
	printf("Arreglo creado con %d elementos\n",N );
	omp_set_num_threads(T);
	#pragma omp parallel
	{
		int tid = omp_get_thread_num();
		int nprocs = omp_get_num_threads();

		for(int i=tid;i<N;i+=nprocs){
			arreglo[i] *= constante;
		}
	}	
	#pragma omp barrier
	printf("Programa finalizado con exito\n");
	/*
	for(int i=0; i<N; i++){
		printf("%d, ", arreglo[i]);
	}
	*/
}
