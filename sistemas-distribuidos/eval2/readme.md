### Nota
Este código fue creado para la asignatura de Sistemas Distribuidos.
fecha de entrega: 07-05-2024
Integrantes: Jonathan Ávila, Enoc Falcón
# Implementación de Lista de Clusters (LC) con OpenMP

Este proyecto desarrolla un índice llamado Lista de Clusters (LC) para indexar elementos multimedia y procesar consultas de manera eficiente. El índice agrupa elementos en clusters utilizando una arquitectura multinúcleo con programación multihilo mediante OpenMP.

## Características

- **Algoritmo de Clustering**: Selecciona centros de clusters y agrupa elementos cercanos basados en la distancia euclidiana.
- **Eficiencia en Consultas**: Permite el descarte rápido de elementos que no son relevantes para una consulta específica.
- **Paralelización**: Utiliza múltiples hilos para calcular distancias y formar clusters de manera concurrente. Utilizando OpenMP.

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
gcc -fopenmp evaluacion2.c -o evaluacion2
./evaluacion2 < test.txt
```
Además se cuentan con 3 archivos con distintos tamaños de entrada

```bash
./evaluacion2 < Unidad-2_LC_test_BD-60.txt
./evaluacion2 < Unidad-2_LC_test_BD-600.txt
./evaluacion2 < Unidad-2_LC_test_BD-6000.txt
```

La entrada del programa debe ser un archivo de texto con la siguiente estructura:

```
<N_elementos>
<K>
<vector1>
<vector2>
...
<vectorN>
```
Siendo K los elementos que componen el cluster sin incluir el centro

## Salida Esperada

El programa imprimirá las coordenadas del centro de cada cluster, el radio de cobertura y las coordenadas de cada elemento en el cluster, uno por línea.

## Notas de Autor

El diseño del programa se creo intentando que fuese modular, creando funciones específicas para cada tarea. Esto facilita la comprensión y el mantenimiento del código. Se optó por implementar dos funciones distintas para la formación de clusters: una para el primer cluster y otra para los clusters restantes. Esta decisión se tomó porque la formación del primer cluster es levemente distinta en su configuración inicial, mientras que la formación de los demás clusters sigue un proceso iterativo y que ademas requiere la identificación de nuevos centros.

Uno de los desafíos más significativos fue la selección de los centros subsecuentes después del primer cluster (C1). Esta tarea implicó el desarrollo de un método eficiente y correcto para calcular y comparar distancias en un entorno paralelizado.

En cuanto a la gestión de memoria, el programa se esfuerza por adherirse a las mejores prácticas y normativas del lenguaje C, garantizando un manejo de memoria seguro y efectivo para evitar fugas y otros problemas comunes.

## Integraciones futuras

- Se podría integrar las dos funciones para la formación de clusters en una sola.
- Agregar marcas de tiempo.
- Entregar información adicional sobre la cantidad de vectores, la cantidad de clusters formados y detalles sobre la máquina en la que se está ejecutando el programa.
- Podría implementarse la escritura de resultados e información de ejecución en un archivo de texto, funcionando como una base de datos.

------------

# Todo
[x] Lectura del archivo<br>
[x] Extracción de la información<br>
[X] Medir las distancias<br>
[X] Encontrar nuevo centrode<br>
[X] Paralelizar Calculo de las distancias<br>