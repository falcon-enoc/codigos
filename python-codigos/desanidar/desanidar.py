#!/usr/bin/env python3

import os
import shutil

def desanidar_archivos():
    directorio_principal = os.getcwd()  # Carpeta actual

    for root, dirs, files in os.walk(directorio_principal, topdown=False):
        if root == directorio_principal:
            continue

        for archivo in files:
            ruta_archivo = os.path.join(root, archivo)
            destino = os.path.join(directorio_principal, archivo)

            # Si ya existe, renombra (archivo (1).txt, archivo (2).txt, etc.)
            if os.path.exists(destino):
                base, ext = os.path.splitext(archivo)
                contador = 1
                nuevo_nombre = f"{base} ({contador}){ext}"
                destino = os.path.join(directorio_principal, nuevo_nombre)
                while os.path.exists(destino):
                    contador += 1
                    nuevo_nombre = f"{base} ({contador}){ext}"
                    destino = os.path.join(directorio_principal, nuevo_nombre)

            shutil.move(ruta_archivo, destino)
            print(f"✅ Movido: {ruta_archivo} → {destino}")

        # Eliminar carpetas vacías
        for carpeta in dirs:
            ruta_carpeta = os.path.join(root, carpeta)
            if not os.listdir(ruta_carpeta):
                os.rmdir(ruta_carpeta)
                print(f"🗑️ Carpeta eliminada: {ruta_carpeta}")

if __name__ == "__main__":
    desanidar_archivos()

