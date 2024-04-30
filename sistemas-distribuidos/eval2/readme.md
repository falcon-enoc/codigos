# Todo
[x] Lectura del archivo<br>
[x] Parsear el archivo<br>
[-] Medir las distancias<br>
[ ] Paralelizar<br>

---

# Implementación de Lista de Clusters (LC) con OpenMP

Este proyecto desarrolla un índice llamado Lista de Clusters (LC) para indexar elementos multimedia y procesar consultas de manera eficiente. El índice agrupa elementos en clusters utilizando una arquitectura multinúcleo con programación multihilo mediante OpenMP.

## Características

- **Algoritmo de Clustering**: Selecciona centros de clusters y agrupa elementos cercanos basados en la distancia euclidiana.
- **Eficiencia en Consultas**: Permite el descarte rápido de elementos que no son relevantes para una consulta específica.
- **Paralelización**: Utiliza múltiples hilos para calcular distancias y formar clusters de manera concurrente.

## Requisitos

- Compilador que soporte OpenMP.
- Sistema operativo compatible con la ejecución de programas en C.

## Configuración

Define la dimensión de los vectores y el número de hilos en el código:

```c
#define DIM 20 // Dimensiones de los vectores
#define N_THREADS 8 // Número de hilos
```

## Uso

Compile el programa con soporte para OpenMP y ejecute con una base de datos de vectores proporcionada:

```bash
gcc -fopenmp tu_programa.c -o tu_programa
./tu_programa < test.txt
```

La entrada del programa debe ser un archivo de texto con la siguiente estructura:

```
<num_elementos>
<K>
<vector1>
<vector2>
...
```

## Salida Esperada

El programa imprimirá las coordenadas del centro de cada cluster, el radio de cobertura y las coordenadas de cada elemento en el cluster, uno por línea.
