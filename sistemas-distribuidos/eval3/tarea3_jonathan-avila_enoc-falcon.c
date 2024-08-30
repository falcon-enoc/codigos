/*
Jonathan Avila
Enoc Falcon
Tarea 3 Sistemas distribuidos
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <mpi.h>

#define DIM 1024
#define K 10

typedef struct {
    double coords[DIM];
} Vector;

// Función para calcular la distancia euclidiana
double euclidean_distance(double *vec1, double *vec2);
void knn_parallel(Vector *database, int N, Vector *queries, int Q, int *result_indices, double *result_distances, int rank, int size);
void insert_neighbor(int *indices, double *distances, int index, double distance);

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double compute_start, compute_end;  // Variables para medir el tiempo de cómputo

    int N, Q;
    Vector *database = NULL;
    Vector *queries = NULL;

    if (rank == 0) {
        scanf("%d", &N);
        database = (Vector *)malloc(N * sizeof(Vector));
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < DIM; j++) {
                scanf("%lf", &database[i].coords[j]);
            }
        }

        scanf("%d", &Q);
        queries = (Vector *)malloc(Q * sizeof(Vector));
        for (int i = 0; i < Q; i++) {
            for (int j = 0; j < DIM; j++) {
                scanf("%lf", &queries[i].coords[j]);
            }
        }
    }

    MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(&Q, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank != 0) {
        database = (Vector *)malloc(N * sizeof(Vector));
        queries = (Vector *)malloc(Q * sizeof(Vector));
    }

    MPI_Bcast(database, N * DIM, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(queries, Q * DIM, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    int *result_indices = (int *)malloc(Q * K * sizeof(int));
    double *result_distances = (double *)malloc(Q * K * sizeof(double));

    compute_start = MPI_Wtime(); 
    knn_parallel(database, N, queries, Q, result_indices, result_distances, rank, size);
    compute_end = MPI_Wtime();

    if (rank == 0) {  // Solo el proceso maestro imprime los resultados
        for (int i = 0; i < Q; i++) {
            printf("Consulta %d:\n", i + 1);
            for (int k = 0; k < K; k++) {
                printf("%d %f\n", result_indices[i * K + k], result_distances[i * K + k]);
            }
        }
        printf("Tiempo de cómputo: %f segundos\n", compute_end - compute_start);
    }

    free(database);
    free(queries);
    free(result_indices);
    free(result_distances);

    MPI_Finalize();
    return 0;
}

void knn_parallel(Vector *database, int N, Vector *queries, int Q, int *result_indices, double *result_distances, int rank, int size) {
    int local_N = N / size;
    int start = rank * local_N;
    int end = (rank == size - 1) ? N : start + local_N;

    for (int q = 0; q < Q; q++) {
        for (int i = 0; i < K; i++) {
            result_distances[q * K + i] = DBL_MAX;
            result_indices[q * K + i] = -1;
        }

        for (int i = start; i < end; i++) {
            double distance = euclidean_distance(database[i].coords, queries[q].coords);
            insert_neighbor(&result_indices[q * K], &result_distances[q * K], i, distance);
        }
    }

    if (rank == 0) {
        int *local_indices = (int *)malloc(Q * K * sizeof(int));
        double *local_distances = (double *)malloc(Q * K * sizeof(double));

        for (int p = 1; p < size; p++) {
            MPI_Recv(local_indices, Q * K, MPI_INT, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Recv(local_distances, Q * K, MPI_DOUBLE, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            for (int q = 0; q < Q; q++) {
                for (int i = 0; i < K; i++) {
                    insert_neighbor(&result_indices[q * K], &result_distances[q * K], local_indices[q * K + i], local_distances[q * K + i]);
                }
            }
        }

        free(local_indices);
        free(local_distances);
    } else {
        MPI_Send(result_indices, Q * K, MPI_INT, 0, 0, MPI_COMM_WORLD);
        MPI_Send(result_distances, Q * K, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
    }
}

void insert_neighbor(int *indices, double *distances, int index, double distance) {
    for (int i = 0; i < K; i++) {
        if (distance < distances[i]) {
            for (int j = K - 1; j > i; j--) {
                distances[j] = distances[j - 1];
                indices[j] = indices[j - 1];
            }
            distances[i] = distance;
            indices[i] = index;
            break;
        }
    }
}

double euclidean_distance(double *vec1, double *vec2) {
    double sum = 0.0;
    for (int i = 0; i < DIM; i++) {
        sum += (vec1[i] - vec2[i]) * (vec1[i] - vec2[i]);
    }
    return sqrt(sum);
}
