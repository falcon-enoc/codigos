#creacion de matriz test para la tarea
import random

def generar_archivo(num_vectores, tamano_cluster):
    vectores_generados = set()
    with open("test.txt", "w") as archivo:
        archivo.write(str(num_vectores) + "\n")
        archivo.write(str(tamano_cluster) + "\n")
        for i in range(num_vectores):
            vector = tuple([round(random.uniform(-1, 1),3) for _ in range(20)])
            if vector not in vectores_generados:
                vectores_generados.add(vector)
                linea = " ".join(map(str, vector))
                if (i == num_vectores-1):
                    archivo.write(linea)
                else:
                    archivo.write(linea + "\n")

# Ejemplo de uso: generar un archivo con 5 vectores
generar_archivo(100, 7)
