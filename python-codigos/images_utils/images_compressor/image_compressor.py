#!/usr/bin/env python3
"""
Compresor de Imágenes
Reduce el tamaño de imágenes manteniendo la calidad visual
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif

# Registrar formatos HEIF/HEIC
pillow_heif.register_heif_opener()

# Formatos soportados
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}

def compress_image(input_path, output_path, quality=85, max_width=None, max_height=None):
    """
    Comprime una imagen individual
    
    Args:
        input_path (str): Ruta de la imagen original
        output_path (str): Ruta donde guardar la imagen comprimida
        quality (int): Calidad de compresión (1-100)
        max_width (int): Ancho máximo opcional
        max_height (int): Alto máximo opcional
    
    Returns:
        tuple: (tamaño_original, tamaño_comprimido, porcentaje_reduccion)
    """
    try:
        # Abrir imagen
        with Image.open(input_path) as img:
            # Corregir orientación EXIF
            img = ImageOps.exif_transpose(img)
            
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if img.mode in ('RGBA', 'P'):
                # Crear fondo blanco para transparencias
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si se especifica
            if max_width or max_height:
                img.thumbnail((max_width or img.width, max_height or img.height), Image.Resampling.LANCZOS)
            
            # Obtener tamaño original
            original_size = os.path.getsize(input_path)
            
            # Guardar imagen comprimida
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Obtener tamaño comprimido
            compressed_size = os.path.getsize(output_path)
            
            # Calcular porcentaje de reducción
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            return original_size, compressed_size, reduction
            
    except Exception as e:
        print(f"Error procesando {input_path}: {e}")
        return None, None, None

def format_size(size_bytes):
    """Formatea el tamaño en bytes a una unidad legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def process_images(input_path, output_dir, quality=85, max_width=None, max_height=None, suffix="_compressed"):
    """
    Procesa imágenes desde un archivo o directorio
    
    Args:
        input_path (str): Ruta del archivo o directorio
        output_dir (str): Directorio de salida
        quality (int): Calidad de compresión
        max_width (int): Ancho máximo opcional
        max_height (int): Alto máximo opcional
        suffix (str): Sufijo para archivos comprimidos
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    
    # Crear directorio de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Lista para almacenar archivos a procesar
    files_to_process = []
    
    if input_path.is_file():
        # Procesar archivo individual
        if input_path.suffix.lower() in SUPPORTED_FORMATS:
            files_to_process.append(input_path)
        else:
            print(f"Formato no soportado: {input_path.suffix}")
            return
    elif input_path.is_dir():
        # Procesar directorio
        for file_path in input_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
                files_to_process.append(file_path)
    else:
        print(f"La ruta no existe: {input_path}")
        return
    
    if not files_to_process:
        print("No se encontraron imágenes para procesar")
        return
    
    print(f"Procesando {len(files_to_process)} imagen(es)...")
    print(f"Calidad: {quality}%")
    if max_width or max_height:
        print(f"Dimensiones máximas: {max_width or 'auto'} x {max_height or 'auto'}")
    print("-" * 60)
    
    total_original = 0
    total_compressed = 0
    processed_count = 0
    
    for file_path in files_to_process:
        # Construir ruta de salida
        if input_path.is_file():
            # Para archivo individual, usar el mismo nombre con sufijo
            output_file = output_dir / f"{file_path.stem}{suffix}.jpg"
        else:
            # Para directorio, mantener estructura relativa
            relative_path = file_path.relative_to(input_path)
            output_file = output_dir / relative_path.with_suffix('.jpg')
            output_file = output_file.with_name(f"{output_file.stem}{suffix}.jpg")
        
        # Crear directorio padre si no existe
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Comprimir imagen
        original_size, compressed_size, reduction = compress_image(
            file_path, output_file, quality, max_width, max_height
        )
        
        if original_size is not None:
            total_original += original_size
            total_compressed += compressed_size
            processed_count += 1
            
            print(f"✓ {file_path.name}")
            print(f"  {format_size(original_size)} → {format_size(compressed_size)} ({reduction:.1f}% reducción)")
        else:
            print(f"✗ Error procesando {file_path.name}")
    
    # Resumen final
    if processed_count > 0:
        total_reduction = ((total_original - total_compressed) / total_original) * 100
        print("-" * 60)
        print(f"Resumen:")
        print(f"Imágenes procesadas: {processed_count}")
        print(f"Tamaño total original: {format_size(total_original)}")
        print(f"Tamaño total comprimido: {format_size(total_compressed)}")
        print(f"Reducción total: {format_size(total_original - total_compressed)} ({total_reduction:.1f}%)")
        print(f"Archivos guardados en: {output_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Compresor de imágenes - Reduce el tamaño manteniendo la calidad visual",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s imagen.jpg -o compressed/
  %(prog)s photos/ -o compressed/ -q 90
  %(prog)s imagen.png -o output/ -q 75 --max-width 1920
  %(prog)s images/ -o compressed/ -q 80 --max-width 1920 --max-height 1080
        """
    )
    
    parser.add_argument('input', help='Archivo de imagen o directorio con imágenes')
    parser.add_argument('-o', '--output', required=True, help='Directorio de salida')
    parser.add_argument('-q', '--quality', type=int, default=85, choices=range(1, 101),
                       help='Calidad de compresión (1-100, default: 85)')
    parser.add_argument('--max-width', type=int, help='Ancho máximo en píxeles')
    parser.add_argument('--max-height', type=int, help='Alto máximo en píxeles')
    parser.add_argument('--suffix', default='_compressed', help='Sufijo para archivos comprimidos (default: _compressed)')
    
    args = parser.parse_args()
    
    # Validar que la entrada existe
    if not os.path.exists(args.input):
        print(f"Error: La ruta '{args.input}' no existe")
        sys.exit(1)
    
    # Procesar imágenes
    process_images(
        args.input, 
        args.output, 
        args.quality, 
        args.max_width, 
        args.max_height, 
        args.suffix
    )

if __name__ == "__main__":
    main()