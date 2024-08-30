#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define DIM 1024
#define K 5

typedef struct {
    double coords[DIM];
} Vector;

// Función para calcular la distancia euclidiana
double euclidean_distance(double *vec1, double *vec2);
void knn_sequential(Vector *database, int N, Vector query, int *result_index, double *result_distance);

int main() {
    int N;
    scanf("%d", &N);

    Vector *database = (Vector *)malloc(N * sizeof(Vector));
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < DIM; j++) {
            scanf("%lf", &database[i].coords[j]);
        }
    }

    int Q;
    scanf("%d", &Q);

    for (int i = 0; i < Q; i++) {
        Vector query;
        for (int j = 0; j < DIM; j++) {
            scanf("%lf", &query.coords[j]);
        }

        int result_index;
        double result_distance;
        knn_sequential(database, N, query, &result_index, &result_distance);
        printf("%d %f\n", result_index, result_distance);
    }

    free(database);
    return 0;
}

void knn_sequential(Vector *database, int N, Vector query, int *result_index, double *result_distance) {
    *result_distance = euclidean_distance(database[0].coords, query.coords);
    *result_index = 0;
    for (int i = 1; i < N; i++) {
        double distance = euclidean_distance(database[i].coords, query.coords);
        if (distance < *result_distance) {
            *result_distance = distance;
            *result_index = i;
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
