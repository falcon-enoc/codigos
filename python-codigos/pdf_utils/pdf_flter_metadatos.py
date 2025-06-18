import os
import shutil
from PyPDF2 import PdfReader

# Función para obtener el año de creación de un archivo PDF
def obtener_ano_creacion(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            info = pdf.metadata
            if info and info.get('/CreationDate'):
                # La fecha está en formato: D:YYYYMMDDHHmmSS (ejemplo: D:20230101235900)
                fecha_creacion = info['/CreationDate']
                ano = fecha_creacion[2:6]  # Extraer el año del formato
                return int(ano)
    except Exception as e:
        print(f"No se pudo leer el archivo {pdf_path}: {e}")
    return None

# Directorios
carpeta_origen = '/Users/enocfalcon/Downloads/pdfs'   # Cambia esto por tu carpeta de origen
carpeta_destino = '/Users/enocfalcon/Downloads/pdfs/utiles'  # Cambia esto por tu carpeta de destino

# Crear la carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Recorrer todos los archivos PDF en la carpeta de origen
for archivo in os.listdir(carpeta_origen):
    if archivo.endswith('.pdf'):
        ruta_pdf = os.path.join(carpeta_origen, archivo)
        ano_creacion = obtener_ano_creacion(ruta_pdf)
        
        # Si el año de creación es 2022, 2023 o 2024, mover el archivo
        if ano_creacion in [2022, 2023, 2024]:
            print(f"Moviendo archivo {archivo} con año de creación {ano_creacion}")
            shutil.move(ruta_pdf, os.path.join(carpeta_destino, archivo))
        else:
            print(f"Archivo {archivo} no corresponde a los años indicados.")
