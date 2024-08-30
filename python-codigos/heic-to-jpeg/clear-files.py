import os
import shutil

def limpiar_carpetas(carpetas):
    """
    Elimina todos los archivos de las carpetas especificadas.

    :param carpetas: Lista de rutas de carpetas que quieres limpiar.
    """
    for carpeta in carpetas:
        for archivo in os.listdir(carpeta):
            ruta_completa = os.path.join(carpeta, archivo)
            
            # Si es un archivo, lo eliminamos
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
                print(f"Archivo eliminado: {ruta_completa}")
            # Si es una carpeta, la eliminamos recursivamente
            elif os.path.isdir(ruta_completa):
                shutil.rmtree(ruta_completa)
                print(f"Carpeta eliminada: {ruta_completa}")

# Ejemplo de uso
carpetas_a_limpiar = [
    "./input",
    "./output"
]

limpiar_carpetas(carpetas_a_limpiar)
