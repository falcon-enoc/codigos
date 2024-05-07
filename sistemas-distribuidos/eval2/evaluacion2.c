/*
Trabajo unidad 2: Listas de clusters
Integrantes:
Jonathan Ávila
Enoc Falcón
*/
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <float.h>
#include <math.h>
#include <omp.h>

#define DIM 20
#define N_THREADS 8

// Definicion de la estructura para guardar la informacion solicitada
typedef struct {
    double **centros;
    double *radios;
    int **member_indices;
    int num_clusters;
} Cluster;

double distancia_euclidiana(double *v1, double *v2);
void inicializar_cluster(Cluster *cluster, int num_vectores, int K);
void liberar_cluster(Cluster *cluster);
void imprimir_clusters(const Cluster *cluster, double **vectores, int K);
void formar_primer_cluster(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados);
void formar_otros_clusters(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados);

int main() {

    int num_vectores, K;
    scanf("%d %d", &num_vectores, &K); // Extraemos las 2 primeras lineas del archivo
    double **db = malloc(num_vectores * sizeof(double *)); // Reserva de memoria para los vectores
    // Extraemos todos los vectores y los alcenamos en db
    for (int i = 0; i < num_vectores; i++) {
        db[i] = malloc(DIM * sizeof(double));
        for (int j = 0; j < DIM; j++) {
            scanf("%lf", &db[i][j]);
        }
    }
    
    // Inicializar cluster
    Cluster cluster;
    inicializar_cluster(&cluster, num_vectores, K);
    
    // Lista para marcar los vectores ya usados
    bool *asignados = calloc(num_vectores, sizeof(bool)); // Inicializa todos los valores en false

    // Formación de Clusters
    formar_primer_cluster(&cluster, db, num_vectores, K, asignados);
    formar_otros_clusters(&cluster, db, num_vectores, K, asignados);

    // Funcion para imprimir la información del cluster
    imprimir_clusters(&cluster, db, K);
    
    // liberar memoria del cluster y lista asignados
    free(asignados);
    liberar_cluster(&cluster);
    
    // liberar memoria de la db
    for (int i = 0; i < num_vectores; i++) {
        free(db[i]);
    }
    free(db);

    return 0;
}

void inicializar_cluster(Cluster *cluster, int num_vectores, int K) {
    // Calcular el número de clústeres basado en el número de vectores y el tamaño de cada clúster
    cluster->num_clusters = ceil((double)num_vectores / (K + 1));

    // Asignar memoria para los centros, radios e índices de miembros
    cluster->centros = malloc(cluster->num_clusters * sizeof(double *));
    cluster->radios = malloc(cluster->num_clusters * sizeof(double));
    cluster->member_indices = malloc(cluster->num_clusters * sizeof(int *));

    for (int i = 0; i < cluster->num_clusters; i++) {
        // Asignar e inicializar cada centro del clúster
        cluster->centros[i] = malloc(DIM * sizeof(double));
        for (int j = 0; j < DIM; j++) {
            cluster->centros[i][j] = 0.0;  // Inicializar el centro a cero
        }

        // Inicializar el radio a 0
        cluster->radios[i] = 0.0;

        // Aquí asumimos que cada clúster puede tener hasta K miembros
        cluster->member_indices[i] = malloc(K * sizeof(int));
    }
}

void liberar_cluster(Cluster *cluster) {
    // Liberar cada uno de los centros
    for (int i = 0; i < cluster->num_clusters; i++) {
        free(cluster->centros[i]);
        // Liberar los índices de miembros de cada clúster
        free(cluster->member_indices[i]);
    }
    // Ahora liberar los arrays de punteros
    free(cluster->centros);
    free(cluster->radios);
    free(cluster->member_indices);

    // Finalmente, resetear los punteros a NULL para evitar el uso de memoria desreferenciada
    cluster->centros = NULL;
    cluster->radios = NULL;
    cluster->member_indices = NULL;
}

double distancia_euclidiana(double *v1, double *v2) {
    double dist = 0.0;
    for (int i = 0; i < DIM; i++) {
        dist += (v1[i] - v2[i]) * (v1[i] - v2[i]);
    }
    return sqrt(dist);
}

void imprimir_clusters(const Cluster *cluster, double **vectores, int K) {
    for (int i = 0; i < cluster->num_clusters; i++) {
        printf("Clúster N°: %d\n", i + 1);
        printf("Centro del clúster:\n[");
        for (int j = 0; j < DIM; j++) {
            printf("%.6lf", cluster->centros[i][j]);  // Usar seis decimales para la precisión
            if (j < DIM - 1) printf(", ");
        }
        printf("]\n");
        printf("Radio del clúster: %lf\n", cluster->radios[i]);

        printf("Elementos del Clúster:\n");
        for (int k = 0; k < K; k++) {  // Asumiendo que siempre hay al menos K miembros en cada clúster
            int idx = cluster->member_indices[i][k];  // Obtener el índice del vector
            printf("[");
            for (int j = 0; j < DIM; j++) {
                printf("%lf", vectores[idx][j]);
                if (j < DIM - 1) printf(", ");
            }
            printf("]\n");
        }
        printf("\n");
    }
}

void formar_primer_cluster(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados) {
    // Copiar el primer vector en el centro del primer clúster (asumiendo que la memoria ya está asignada)
    for (int i = 0; i < DIM; i++) {
        cluster->centros[0][i] = vectores[0][i];
    }

    double *distancias = malloc(num_vectores * sizeof(double));
    omp_set_num_threads(N_THREADS);
    #pragma omp parallel for
    for (int i = 0; i < num_vectores; i++) {
        distancias[i] = distancia_euclidiana(cluster->centros[0], vectores[i]);
    }

    for (int i = 0; i < K; i++) {
        double min_dist = DBL_MAX;
        int min_index = -1;
        for (int j = 0; j < num_vectores; j++) {
            if (!asignados[j] && distancias[j] < min_dist) {
                min_dist = distancias[j];
                min_index = j;
            }
        }
        if (min_index != -1) {  // Verificar si encontramos un vector no asignado
            cluster->member_indices[0][i] = min_index;
            asignados[min_index] = true;  // Marcar como asignado
            distancias[min_index] = DBL_MAX;  // Esto es opcional ya que el vector ya está marcado como asignado
        }
    }

    cluster->radios[0] = 0;
    for (int i = 0; i < K; i++) {
        int idx = cluster->member_indices[0][i];
        double dist = distancia_euclidiana(cluster->centros[0], vectores[idx]);
        if (dist > cluster->radios[0]) {
            cluster->radios[0] = dist;
        }
    }

    free(distancias);
}

void formar_otros_clusters(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados) {
    for (int c = 1; c < cluster->num_clusters; c++) {
        // Inicializar el centro del nuevo clúster
        double max_dist = 0;
        int max_index = 0;
        for (int i = 0; i < num_vectores; i++) {
            double dist = distancia_euclidiana(cluster->centros[c-1], vectores[i]);
            if (dist > max_dist) {
                max_dist = dist;
                max_index = i;
            }
        }
        for (int i = 0; i < DIM; i++) {
            cluster->centros[c][i] = vectores[max_index][i];
        }

        double *distancias = malloc(num_vectores * sizeof(double));
        omp_set_num_threads(N_THREADS);
        #pragma omp parallel for
        for (int i = 0; i < num_vectores; i++) {
            distancias[i] = distancia_euclidiana(cluster->centros[c], vectores[i]);
        }

    for (int i = 0; i < K; i++) {
        double min_dist = DBL_MAX;
        int min_index = -1;
        for (int j = 0; j < num_vectores; j++) {
            if (!asignados[j] && distancias[j] < min_dist) {
                min_dist = distancias[j];
                min_index = j;
            }
        }
        if (min_index != -1) {
            cluster->member_indices[c][i] = min_index;
            asignados[min_index] = true;
            distancias[min_index] = DBL_MAX;
        }
    }

        cluster->radios[c] = 0;
        for (int i = 0; i < K; i++) {
            int idx = cluster->member_indices[c][i];
            double dist = distancia_euclidiana(cluster->centros[c], vectores[idx]);
            if (dist > cluster->radios[c]) {
                cluster->radios[c] = dist;
            }
        }

        free(distancias);
    }
}