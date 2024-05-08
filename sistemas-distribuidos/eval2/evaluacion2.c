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
    
    // Liberar memoria del cluster y lista asignados
    free(asignados);
    liberar_cluster(&cluster);
    
    // Liberar memoria de la db
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
    // Esta funcion se encarga de liberar la memoria asignada a cada parte de la estructura cluster
    for (int i = 0; i < cluster->num_clusters; i++) {
        free(cluster->centros[i]);
        free(cluster->member_indices[i]);
    }

    free(cluster->centros);
    free(cluster->radios);
    free(cluster->member_indices);

    cluster->centros = NULL;
    cluster->radios = NULL;
    cluster->member_indices = NULL;
}

double distancia_euclidiana(double *v1, double *v2) {
    // Calcula la distancia ecludiana entre 2 vectores de dimension igual a DIM (20)
    double dist = 0.0;
    for (int i = 0; i < DIM; i++) {
        dist += (v1[i] - v2[i]) * (v1[i] - v2[i]);
    }
    return sqrt(dist);
}

void imprimir_clusters(const Cluster *cluster, double **vectores, int K) {
    // Imprime deacuerdo a lo solicitado
    printf("------------\n");
    for (int i = 0; i < cluster->num_clusters; i++) {
        //printf("Clúster N°: %d\n", i + 1);
        //printf("Centro del clúster:\n[");
        printf("[");
        for (int j = 0; j < DIM; j++) {
            printf("%.4lf", cluster->centros[i][j]);
            if (j < DIM - 1) printf(", ");
        }
        printf("]\n");
        //printf("Radio del clúster: %lf\n", cluster->radios[i]);
        printf("%lf\n", cluster->radios[i]);

        //printf("Elementos del Clúster:\n");
        for (int k = 0; k < K; k++) {  // Asumiendo que siempre hay al menos K miembros en cada clúster
            int idx = cluster->member_indices[i][k];  // Obtener el índice del vector
            printf("[");
            for (int j = 0; j < DIM; j++) {
                printf("%lf", vectores[idx][j]);
                if (j < DIM - 1) printf(", ");
            }
            printf("]\n");
        }
        printf("------------\n");
    }
}

void formar_primer_cluster(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados) {
    // Establecer el primer vector del conjunto de datos como el centro del primer cluster
    for (int i = 0; i < DIM; i++) {
        cluster->centros[0][i] = vectores[0][i];
    }

    // Array para almacenar las distancias de todos los vectores al centro del primer cluster
    double *distancias = malloc(num_vectores * sizeof(double));
    // Configurar el número de hilos para la paralelización con OpenMP
    omp_set_num_threads(N_THREADS);
    // Calcular paralelamente las distancias Euclidianas desde el centro del primer cluster
    #pragma omp parallel for
    for (int i = 0; i < num_vectores; i++) {
        distancias[i] = distancia_euclidiana(cluster->centros[0], vectores[i]);
    }

    // Elegir los K vectores más cercanos al centro que aún no están asignados a ningún cluster
    for (int i = 0; i < K; i++) {
        double min_dist = DBL_MAX;
        int min_index = -1;
        for (int j = 0; j < num_vectores; j++) {
            if (!asignados[j] && distancias[j] < min_dist) {
                min_dist = distancias[j];
                min_index = j;
            }
        }
        // Verificar si se encontró un vector adecuado para ser asignado al cluster
        if (min_index != -1) {
            cluster->member_indices[0][i] = min_index;
            asignados[min_index] = true;  // Marcar el vector como asignado
            distancias[min_index] = DBL_MAX;  // Evitar que se vuelva a seleccionar
        }
    }

    // Calcular el radio del cluster como la máxima distancia entre el centro y los miembros del cluster
    cluster->radios[0] = 0;
    for (int i = 0; i < K; i++) {
        int idx = cluster->member_indices[0][i];
        double dist = distancia_euclidiana(cluster->centros[0], vectores[idx]);
        if (dist > cluster->radios[0]) {
            cluster->radios[0] = dist;
        }
    }

    // Liberar el array de distancias después de su uso
    free(distancias);
}

void formar_otros_clusters(Cluster *cluster, double **vectores, int num_vectores, int K, bool *asignados) {
    bool *centros_asignados = malloc(num_vectores * sizeof(bool));
    // Formar los clusters subsiguientes
    for (int c = 1; c < cluster->num_clusters; c++) {
        // Buscar el vector más alejado del último centro de cluster formado y usarlo como nuevo centro
        double max_dist = 0;
        int max_index = 0;
        for (int i = 0; i < num_vectores; i++) {
            if (!centros_asignados[i]){
                double dist = distancia_euclidiana(cluster->centros[c-1], vectores[i]);
                if (dist > max_dist) {
                    max_dist = dist;
                    max_index = i;
                }
            }
        }
        // Establecer el vector más distante como el centro del nuevo cluster
        for (int i = 0; i < DIM; i++) {
            cluster->centros[c][i] = vectores[max_index][i];
        }

        centros_asignados[max_index] = true;

        // Calcular las distancias de todos los vectores al nuevo centro del cluster
        double *distancias = malloc(num_vectores * sizeof(double));
        omp_set_num_threads(N_THREADS);
        #pragma omp parallel for
        for (int i = 0; i < num_vectores; i++) {
            distancias[i] = distancia_euclidiana(cluster->centros[c], vectores[i]);
        }

        // Seleccionar los K vectores más cercanos al nuevo centro que no estén asignados
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
                asignados[min_index] = true;  // Marcar el vector como asignado
                distancias[min_index] = DBL_MAX;  // Evitar su reselección
            }
        }

        // Determinar el radio del nuevo cluster
        cluster->radios[c] = 0;
        for (int i = 0; i < K; i++) {
            int idx = cluster->member_indices[c][i];
            double dist = distancia_euclidiana(cluster->centros[c], vectores[idx]);
            if (dist > cluster->radios[c]) {
                cluster->radios[c] = dist;
            }
        }

        // Liberar el array de distancias después de su uso
        free(distancias);
    }
}