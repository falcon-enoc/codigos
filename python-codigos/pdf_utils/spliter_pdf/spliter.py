#!/usr/bin/env python3
"""
PDF Splitter - Herramienta para separar archivos PDF en segmentos específicos

Uso:
    python spliter.py archivo.pdf --segmentos "1-5" "10-15" "20-25"
    python spliter.py archivo.pdf -s "1-3" "7-9" --output-dir salida/
"""

import argparse
import os
import sys
from pathlib import Path
try:
    from PyPDF2 import PdfReader, PdfWriter
except ImportError:
    print("Error: PyPDF2 no está instalado. Ejecuta: pip install PyPDF2")
    sys.exit(1)


def validar_archivo_pdf(archivo):
    """Valida que el archivo existe y es un PDF válido"""
    if not os.path.exists(archivo):
        raise FileNotFoundError(f"El archivo {archivo} no existe")
    
    if not archivo.lower().endswith('.pdf'):
        raise ValueError(f"El archivo {archivo} no es un PDF")
    
    try:
        reader = PdfReader(archivo)
        return len(reader.pages)
    except Exception as e:
        raise ValueError(f"Error al leer el PDF: {e}")


def parsear_segmento(segmento, total_paginas):
    """
    Convierte un string de segmento a rango de páginas
    Formatos soportados:
    - "5" -> página 5
    - "1-5" -> páginas 1 a 5
    - "10-" -> desde página 10 hasta el final
    - "-5" -> desde el inicio hasta página 5
    """
    segmento = segmento.strip()
    
    if '-' not in segmento:
        # Una sola página
        try:
            pagina = int(segmento)
            if 1 <= pagina <= total_paginas:
                return (pagina, pagina)
            else:
                raise ValueError(f"Página {pagina} fuera de rango (1-{total_paginas})")
        except ValueError:
            raise ValueError(f"Formato de página inválido: {segmento}")
    
    # Rango de páginas
    partes = segmento.split('-', 1)
    inicio_str, fin_str = partes[0], partes[1]
    
    # Determinar página de inicio
    if inicio_str == '':
        inicio = 1
    else:
        try:
            inicio = int(inicio_str)
        except ValueError:
            raise ValueError(f"Página de inicio inválida: {inicio_str}")
    
    # Determinar página de fin
    if fin_str == '':
        fin = total_paginas
    else:
        try:
            fin = int(fin_str)
        except ValueError:
            raise ValueError(f"Página de fin inválida: {fin_str}")
    
    # Validar rango
    if inicio < 1 or fin > total_paginas or inicio > fin:
        raise ValueError(f"Rango inválido: {inicio}-{fin} (total páginas: {total_paginas})")
    
    return (inicio, fin)


def crear_pdf_segmento(archivo_entrada, inicio, fin, archivo_salida):
    """Crea un nuevo PDF con las páginas del segmento especificado"""
    reader = PdfReader(archivo_entrada)
    writer = PdfWriter()
    
    # Agregar páginas del segmento (convertir de 1-indexado a 0-indexado)
    for i in range(inicio - 1, fin):
        writer.add_page(reader.pages[i])
    
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    
    # Escribir el archivo
    with open(archivo_salida, 'wb') as archivo_out:
        writer.write(archivo_out)
    
    return len(writer.pages)


def separar_pdf(archivo_entrada, segmentos, directorio_salida=None):
    """
    Separa un PDF en múltiples archivos según los segmentos especificados
    
    Args:
        archivo_entrada (str): Ruta del archivo PDF de entrada
        segmentos (list): Lista de strings con los segmentos a extraer
        directorio_salida (str): Directorio donde guardar los archivos
    
    Returns:
        list: Lista de archivos creados
    """
    print(f"Procesando archivo: {archivo_entrada}")
    
    # Validar archivo de entrada
    total_paginas = validar_archivo_pdf(archivo_entrada)
    print(f"Total de páginas: {total_paginas}")
    
    # Configurar directorio de salida
    if directorio_salida is None:
        directorio_salida = os.path.dirname(archivo_entrada) or '.'
    
    nombre_base = Path(archivo_entrada).stem
    
    # Procesar cada segmento
    archivos_creados = []
    
    for i, segmento in enumerate(segmentos, 1):
        try:
            inicio, fin = parsear_segmento(segmento, total_paginas)
            
            # Generar nombre del archivo de salida
            if inicio == fin:
                nombre_salida = f"{nombre_base}_pagina_{inicio}.pdf"
            else:
                nombre_salida = f"{nombre_base}_paginas_{inicio}-{fin}.pdf"
            
            archivo_salida = os.path.join(directorio_salida, nombre_salida)
            
            # Crear el segmento
            paginas_extraidas = crear_pdf_segmento(archivo_entrada, inicio, fin, archivo_salida)
            
            print(f"Segmento {i}: Páginas {inicio}-{fin} -> {archivo_salida} ({paginas_extraidas} páginas)")
            archivos_creados.append(archivo_salida)
            
        except Exception as e:
            print(f"Error procesando segmento '{segmento}': {e}")
            continue
    
    return archivos_creados


def main():
    parser = argparse.ArgumentParser(
        description="Separar archivos PDF en segmentos específicos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python spliter.py documento.pdf -s "1-5" "10-15" "20"
  python spliter.py archivo.pdf --segmentos "1-3" "7-" "-5" --output-dir salida/
  python spliter.py test.pdf -s "1" "3" "5-7" "10-"

Formatos de segmentos:
  "5"     -> Solo la página 5
  "1-5"   -> Páginas 1 a 5
  "10-"   -> Desde página 10 hasta el final
  "-5"    -> Desde el inicio hasta página 5
        """
    )
    
    parser.add_argument('archivo', help='Archivo PDF de entrada')
    parser.add_argument('-s', '--segmentos', nargs='+', required=True,
                       help='Segmentos a extraer (ej: "1-5" "10-15" "20")')
    parser.add_argument('-o', '--output-dir', dest='directorio_salida',
                       help='Directorio de salida (por defecto: mismo directorio del archivo)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Mostrar información detallada')
    
    args = parser.parse_args()
    
    try:
        # Validar argumentos
        if not args.segmentos:
            print("Error: Debe especificar al menos un segmento")
            return 1
        
        # Separar PDF
        archivos_creados = separar_pdf(
            args.archivo, 
            args.segmentos, 
            args.directorio_salida
        )
        
        # Mostrar resultados
        if archivos_creados:
            print(f"\n✅ Se crearon {len(archivos_creados)} archivos:")
            for archivo in archivos_creados:
                print(f"  - {archivo}")
        else:
            print("❌ No se creó ningún archivo")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())