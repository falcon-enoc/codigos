#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <mpi.h>

#define DIM 1024
#define K 5

typedef struct {
    double coords[DIM];
} Vector;

// Función para calcular la distancia euclidiana
double euclidean_distance(double *vec1, double *vec2);
void knn_parallel(Vector *database, int N, Vector *queries, int Q, int **result_indices, double **result_distances, int rank, int size);
void insert_neighbor(int *indices, double *distances, int index, double distance);

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

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
    }
    MPI_Bcast(database, N * DIM, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    int local_Q = Q / size;
    int start_query = rank * local_Q;
    int end_query = (rank == size - 1) ? Q : start_query + local_Q;

    Vector *local_queries = (Vector *)malloc(local_Q * sizeof(Vector));
    MPI_Scatter(queries, local_Q * DIM, MPI_DOUBLE, local_queries, local_Q * DIM, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    int **result_indices = (int **)malloc(local_Q * sizeof(int *));
    double **result_distances = (double **)malloc(local_Q * sizeof(double *));
    for (int i = 0; i < local_Q; i++) {
        result_indices[i] = (int *)malloc(K * sizeof(int));
        result_distances[i] = (double *)malloc(K * sizeof(double));
    }

    knn_parallel(database, N, local_queries, local_Q, result_indices, result_distances, rank, size);

    if (rank == 0) {
        int **final_indices = (int **)malloc(Q * sizeof(int *));
        double **final_distances = (double **)malloc(Q * sizeof(double *));
        for (int i = 0; i < Q; i++) {
            final_indices[i] = (int *)malloc(K * sizeof(int));
            final_distances[i] = (double *)malloc(K * sizeof(double));
        }

        MPI_Gather(MPI_IN_PLACE, local_Q * K, MPI_INT, final_indices[0], local_Q * K, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Gather(MPI_IN_PLACE, local_Q * K, MPI_DOUBLE, final_distances[0], local_Q * K, MPI_DOUBLE, 0, MPI_COMM_WORLD);

        for (int i = 0; i < Q; i++) {
            for (int k = 0; k < K; k++) {
                printf("%d %f\n", final_indices[i][k], final_distances[i][k]);
            }
        }

        for (int i = 0; i < Q; i++) {
            free(final_indices[i]);
            free(final_distances[i]);
        }
        free(final_indices);
        free(final_distances);
    } else {
        MPI_Gather(result_indices[0], local_Q * K, MPI_INT, NULL, 0, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Gather(result_distances[0], local_Q * K, MPI_DOUBLE, NULL, 0, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    }

    for (int i = 0; i < local_Q; i++) {
        free(result_indices[i]);
        free(result_distances[i]);
    }
    free(result_indices);
    free(result_distances);

    free(database);
    free(local_queries);

    MPI_Finalize();
    return 0;
}

void knn_parallel(Vector *database, int N, Vector *queries, int Q, int **result_indices, double **result_distances, int rank, int size) {
    for (int q = 0; q < Q; q++) {
        for (int i = 0; i < K; i++) {
            result_distances[q][i] = DBL_MAX;
            result_indices[q][i] = -1;
        }

        for (int i = 0; i < N; i++) {
            double distance = euclidean_distance(database[i].coords, queries[q].coords);
            insert_neighbor(result_indices[q], result_distances[q], i, distance);
        }
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
