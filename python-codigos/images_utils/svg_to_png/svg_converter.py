#!/usr/bin/env python3
"""
Script para convertir imágenes SVG a PNG o JPEG
"""

import argparse
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Tuple

try:
    import cairosvg
    from PIL import Image
    import xml.etree.ElementTree as ET
except ImportError as e:
    print("Error: Falta instalar dependencias en tu entorno (venv).")
    print("Sugerencia: activa tu venv y ejecuta: pip install .  (o pip install -r requirements.txt)")
    print(f"Detalle: {e}")
    sys.exit(1)


def validate_svg(svg_path: str) -> Tuple[bool, str]:
    """
    Valida si un archivo SVG es XML bien formado.

    Returns:
        (es_valido, mensaje_error)
    """
    try:
        # Leer como binario y decodificar con utf-8, luego fallback a latin-1
        with open(svg_path, 'rb') as f:
            data = f.read()
        try:
            content = data.decode('utf-8')
        except UnicodeDecodeError:
            content = data.decode('latin-1')

        ET.fromstring(content)
        return True, ""
    except FileNotFoundError:
        return False, "Archivo no encontrado"
    except ET.ParseError as e:
        return False, "Error de sintaxis XML: %s" % e
    except Exception as e:
        return False, "Error al validar: %s" % e


def _rsvg_convert_to_png(svg_path: str, output_path: str, scale: float = 1.0) -> bool:
    """Conversión usando rsvg-convert (librsvg)."""
    cmd = [
        'rsvg-convert',
        '-f', 'png',
        '-o', output_path,
        '-z', str(scale),
        svg_path,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print("✗ Fallback rsvg-convert falló: %s" % e)
        return False


def convert_svg_to_png(svg_path: str, output_path: str, scale: float = 1.0, backend: str = 'auto') -> bool:
    """
    Convierte un archivo SVG a PNG
    """
    try:
        if backend in ('auto', 'cairosvg'):
            cairosvg.svg2png(url=svg_path, write_to=output_path, scale=scale)
            print("✓ Convertido: %s -> %s" % (svg_path, output_path))
            return True
    except Exception as e:
        # Intentar fallback si corresponde
        if backend == 'auto' and shutil.which('rsvg-convert'):
            print("⚠ CairoSVG falló, intentando con rsvg-convert...")
            ok = _rsvg_convert_to_png(svg_path, output_path, scale)
            if ok:
                print("✓ Convertido (fallback rsvg): %s -> %s" % (svg_path, output_path))
                return True
        print("✗ Error al convertir %s: %s" % (svg_path, e))
        return False


def convert_svg_to_jpeg(svg_path: str, output_path: str, scale: float = 1.0, quality: int = 95, backend: str = 'auto') -> bool:
    """
    Convierte un archivo SVG a JPEG
    """
    try:
        png_image = None
        if backend in ('auto', 'cairosvg'):
            # Primero convertimos a PNG en memoria con CairoSVG
            from io import BytesIO
            png_data = cairosvg.svg2png(url=svg_path, scale=scale)
            png_image = Image.open(BytesIO(png_data))
        else:
            raise RuntimeError('Forzar rsvg')

        # Convertir RGBA a RGB si es necesario (JPEG no soporta transparencia)
        if png_image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', png_image.size, (255, 255, 255))
            if png_image.mode == 'P':
                png_image = png_image.convert('RGBA')
            background.paste(png_image, mask=png_image.split()[-1] if png_image.mode in ('RGBA', 'LA') else None)
            png_image = background

        png_image.save(output_path, 'JPEG', quality=quality)
        print("✓ Convertido: %s -> %s" % (svg_path, output_path))
        return True
    except Exception as e:
        # Fallback rsvg -> PNG temporal, luego a JPEG
        if backend == 'auto' and shutil.which('rsvg-convert'):
            print("⚠ CairoSVG falló, intentando con rsvg-convert...")
            tmp_png = None
            try:
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    tmp_png = tmp.name
                ok = _rsvg_convert_to_png(svg_path, tmp_png, scale)
                if ok:
                    img = Image.open(tmp_png)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        bg.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = bg
                    img.save(output_path, 'JPEG', quality=quality)
                    print("✓ Convertido (fallback rsvg): %s -> %s" % (svg_path, output_path))
                    return True
            except Exception as e2:
                print("✗ Error en fallback rsvg: %s" % e2)
            finally:
                if tmp_png and os.path.exists(tmp_png):
                    try:
                        os.remove(tmp_png)
                    except Exception:
                        pass
        print("✗ Error al convertir %s: %s" % (svg_path, e))
        return False


def get_output_path(input_path: str, output_dir: str = None, output_format: str = 'png') -> str:
    """
    Genera la ruta de salida para el archivo convertido
    """
    input_file = Path(input_path)
    output_extension = ".%s" % output_format.lower()

    if output_dir:
        output_directory = Path(output_dir)
        output_directory.mkdir(parents=True, exist_ok=True)
        output_file = output_directory / ("%s%s" % (input_file.stem, output_extension))
    else:
        output_file = input_file.parent / ("%s%s" % (input_file.stem, output_extension))

    return str(output_file)


def process_files(input_files: List[str], output_dir: str = None,
                  output_format: str = 'png', scale: float = 1.0,
                  quality: int = 95, backend: str = 'auto', skip_validation: bool = False) -> None:
    """
    Procesa una lista de archivos SVG
    """
    success_count = 0
    fail_count = 0

    print("\n" + ("=" * 60))
    print("Convirtiendo %d archivo(s) SVG a %s" % (len(input_files), output_format.upper()))
    print(("=" * 60) + "\n")

    for svg_file in input_files:
        if not os.path.exists(svg_file):
            print("✗ Archivo no encontrado: %s" % svg_file)
            fail_count += 1
            continue

        if not svg_file.lower().endswith('.svg'):
            print("⚠ Advertencia: %s no es un archivo SVG, se omite" % svg_file)
            continue

        # Validación opcional del SVG
        if not skip_validation:
            is_valid, error_msg = validate_svg(svg_file)
            if not is_valid:
                print("✗ SVG inválido: %s" % svg_file)
                print("  %s" % error_msg)
                print("  Sugerencia: Abre el archivo en un editor SVG y corrígelo, o prueba con https://jakearchibald.github.io/svgomg/")
                fail_count += 1
                continue

        output_path = get_output_path(svg_file, output_dir, output_format)

        if output_format.lower() == 'png':
            success = convert_svg_to_png(svg_file, output_path, scale, backend)
        elif output_format.lower() in ('jpeg', 'jpg'):
            success = convert_svg_to_jpeg(svg_file, output_path, scale, quality, backend)
        else:
            print("✗ Formato no soportado: %s" % output_format)
            fail_count += 1
            continue

        if success:
            success_count += 1
        else:
            fail_count += 1

    print("\n" + ("=" * 60))
    print("Resumen: %d exitoso(s), %d fallido(s)" % (success_count, fail_count))
    print(("=" * 60) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Convierte imágenes SVG a PNG o JPEG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s imagen.svg
  %(prog)s imagen1.svg imagen2.svg imagen3.svg
  %(prog)s *.svg -o ./salida
  %(prog)s imagen.svg -f jpeg -o ./salida
  %(prog)s imagen.svg -f png -s 2.0 -o ./salida
  %(prog)s imagen.svg -f jpeg -q 90
        """
    )

    parser.add_argument(
        'input_files',
        nargs='+',
        help='Archivo(s) SVG a convertir'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        default=None,
        help='Directorio de salida (por defecto: misma ubicación que el archivo de entrada)'
    )

    parser.add_argument(
        '-f', '--format',
        dest='format',
        choices=['png', 'jpeg', 'jpg'],
        default='png',
        help='Formato de salida (por defecto: png)'
    )

    parser.add_argument(
        '-s', '--scale',
        dest='scale',
        type=float,
        default=1.0,
        help='Factor de escala para el tamaño de salida (por defecto: 1.0)'
    )

    parser.add_argument(
        '-q', '--quality',
        dest='quality',
        type=int,
        default=95,
        help='Calidad para JPEG (1-100, por defecto: 95)'
    )

    parser.add_argument(
        '--backend',
        dest='backend',
        choices=['auto', 'cairosvg', 'rsvg'],
        default='auto',
        help='Backend de conversión: auto (intenta CairoSVG y luego rsvg), cairosvg, rsvg'
    )

    parser.add_argument(
        '--skip-validation',
        dest='skip_validation',
        action='store_true',
        help='Omite la validación XML del SVG (útil si el backend rsvg tolera el archivo)'
    )

    args = parser.parse_args()

    # Validar calidad
    if not 1 <= args.quality <= 100:
        print("Error: La calidad debe estar entre 1 y 100")
        sys.exit(1)

    # Validar escala
    if args.scale <= 0:
        print("Error: El factor de escala debe ser mayor que 0")
        sys.exit(1)

    # Normalizar formato
    output_format = 'jpeg' if args.format in ('jpeg', 'jpg') else 'png'

    # Procesar archivos
    process_files(
        args.input_files,
        args.output_dir,
        output_format,
        args.scale,
        args.quality,
        args.backend,
        args.skip_validation,
    )


if __name__ == '__main__':
    main()
def _rsvg_convert_to_png(svg_path: str, output_path: str, scale: float = 1.0) -> bool:
    """Conversión usando rsvg-convert (librsvg)."""
    cmd = [
        'rsvg-convert',
        '-f', 'png',
        '-o', output_path,
        '-z', str(scale),
        svg_path,
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print("✗ Fallback rsvg-convert falló: %s" % e)
        return False

    
    Args:
        svg_path: Ruta del archivo SVG
    
    Returns:
        Tupla (es_válido, mensaje_de_error)
    """
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Intentar parsear como XML
        ET.fromstring(content)
        return True, ""
    except ET.ParseError as e:
        return False, f"Error de sintaxis XML: {e}"
    except UnicodeDecodeError:
        # Intentar con otra codificación
        error_msg = str(e)
        if "unclosed token" in error_msg or "not well-formed" in error_msg:
            print(f"✗ Error al convertir {svg_path}: El archivo SVG tiene errores de sintaxis XML")
            print(f"  Sugerencia: Abre el archivo en un editor SVG (Inkscape, Adobe Illustrator) y guárdalo de nuevo")
        elif "No such file" in error_msg:
            print(f"✗ Error al convertir {svg_path}: Archivo no encontrado")
        else:
            print(f"✗ Error al convertir {svg_path}: {error_msg
            with open(svg_path, 'r', encoding='latin-1') as f:
                content = f.read()
            ET.fromstring(content)
            return True, ""
        except Exception as e:
            return False, f"Error de codificación: {e}"
    except Exception as e:
        return False, f"Error al validar: {e}"


def convert_svg_to_png(svg_path: str, output_path: str, scale: float = 1.0) -> bool:
    """
    Convierte un archivo SVG a PNG
    
    Args:
        svg_path: Ruta del archivo SVG de entrada
        output_path: Ruta del archivo PNG de salida
        scale: Factor de escala para el tamaño de salida
    
    Returns:
        True si la conversión fue exitosa, False en caso contrario
    """
    try:
        cairosvg.svg2png(
            url=svg_path,
            write_to=output_path,
            scale=scale
        )
        print(f"✓ Convertido: {svg_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error al convertir {svg_path}: {e}")
        return False


def convert_svg_to_jpeg(svg_path: str, output_path: str, scale: float = 1.0, quality: int = 95) -> bool:
    """
    Convierte un archivo SVG a JPEG
    
    Args:
        svg_path: Ruta del archivo SVG de entrada
        output_path: Ruta del archivo JPEG de salida
        scale: Factor de escala para el tamaño de salida
        quality: Calidad del JPEG (1-100)
    
    Returns:
        True si la conversión fue exitosa, False en caso contrario
    """
    try:
        # Primero convertimos a PNG en memoria
        png_data = cairosvg.svg2png(url=svg_path, scale=scale)
        
        # Luego convertimos PNG a JPEG usando Pillow
        from io import BytesIO
        png_image = Image.open(BytesIO(png_data))
        
        # Convertir RGBA a RGB si es necesario (JPEG no soporta transparencia)
        if png_image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', png_image.size, (255, 255, 255))
            if png_image.mode == 'P':
                png_image = png_image.convert('RGBA')
        error_msg = str(e)
        if "unclosed token" in error_msg or "not well-formed" in error_msg:
            print(f"✗ Error al convertir {svg_path}: El archivo SVG tiene errores de sintaxis XML")
            print(f"  Sugerencia: Abre el archivo en un editor SVG (Inkscape, Adobe Illustrator) y guárdalo de nuevo")
        elif "No such file" in error_msg:
            print(f"✗ Error al convertir {svg_path}: Archivo no encontrado")
        else:
            print(f"✗ Error al convertir {svg_path}: {error_msgage.split()[-1] if png_image.mode in ('RGBA', 'LA') else None)
            png_image = background
        
        png_image.save(output_path, 'JPEG', quality=quality)
        print(f"✓ Convertido: {svg_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error al convertir {svg_path}: {e}")
        return False


def get_output_path(input_path: str, output_dir: str = None, output_format: str = 'png') -> str:
    """
    Genera la ruta de salida para el archivo convertido
    
    Args:
        input_path: Ruta del archivo de entrada
        output_dir: Directorio de salida (opcional)
        output_format: Formato de salida ('png' o 'jpeg')
    
    Returns:
        Ruta completa del archivo de salida
    """
    input_file = Path(input_path)
    output_extension = f'.{output_format.lower()}'
    
    if output_dir:
        output_directory = Path(output_dir)
        output_directory.mkdir(parents=True, exist_ok=True)
        output_file = output_directory / f"{input_file.stem}{output_extension}"
    else:
        output_file = input_file.parent / f"{input_file.stem}{output_extension}"
    
    return str(output_file)


def process_files(input_files: List[str], output_dir: str = None, 
                  output_format: str = 'png', scale: float = 1.0, 
                  quality: int = 95) -> None:
    """
    Procesa una lista de archivos SVG
    
    Args:
        input_files: Lista de rutas de archivos SVG
        output_dir: Directorio de salida (opcional)
        output_format: Formato de salida ('png' o 'jpeg')
        scale: Factor de escala
        quality: Calidad para JPEG
    """
    success_count = 0
    fail_count = 0
    
    prin# Validar SVG antes de intentar convertir
        is_valid, error_msg = validate_svg(svg_file)
        if not is_valid:
            print(f"✗ SVG inválido: {svg_file}")
            print(f"  {error_msg}")
            print(f"  Sugerencia: Abre el archivo en un editor SVG y corrígelo, o prueba con https://jakearchibald.github.io/svgomg/")
            fail_count += 1
            continue
        
        t(f"\n{'='*60}")
    print(f"Convirtiendo {len(input_files)} archivo(s) SVG a {output_format.upper()}")
    print(f"{'='*60}\n")
    
    for svg_file in input_files:
        if not os.path.exists(svg_file):
            print(f"✗ Archivo no encontrado: {svg_file}")
            fail_count += 1
            continue
        
        if not svg_file.lower().endswith('.svg'):
            print(f"⚠ Advertencia: {svg_file} no es un archivo SVG, se omite")
            continue
        # Validación opcional del SVG
        if not skip_validation:
            is_valid, error_msg = validate_svg(svg_file)
            if not is_valid:
                print("✗ SVG inválido: %s" % svg_file)
                print("  %s" % error_msg)
                print("  Sugerencia: Abre el archivo en un editor SVG y corrígelo, o prueba con https://jakearchibald.github.io/svgomg/")
                fail_count += 1
                continue

        output_path = get_output_path(svg_file, output_dir, output_format)
        

    parser.add_argument(
        '--backend',
        dest='backend',
        choices=['auto', 'cairosvg', 'rsvg'],
        default='auto',
        help='Backend de conversión: auto (intenta CairoSVG y luego rsvg), cairosvg, rsvg'
    )

    parser.add_argument(
        '--skip-validation',
        dest='skip_validation',
        action='store_true',
        help='Omite la validación XML del SVG (útil si el backend rsvg tolera el archivo)'
    )
        if output_format.lower() == 'png':
            success = convert_svg_to_png(svg_file, output_path, scale)
        elif output_format.lower() in ('jpeg', 'jpg'):
            success = convert_svg_to_jpeg(svg_file, output_path, scale, quality)
        else:
            print(f"✗ Formato no soportado: {output_format}")
            fail_count += 1
            continue
        
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"Resumen: {success_count} exitoso(s), {fail_count} fallido(s)")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Convierte imágenes SVG a PNG o JPEG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        args.backend,
        args.skip_validation,
        epilog="""
Ejemplos de uso:
  %(prog)s imagen.svg
  %(prog)s imagen1.svg imagen2.svg imagen3.svg
  %(prog)s *.svg -o ./salida
  %(prog)s imagen.svg -f jpeg -o ./salida
  %(prog)s imagen.svg -f png -s 2.0 -o ./salida
  %(prog)s imagen.svg -f jpeg -q 90
        """
    )
    
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Archivo(s) SVG a convertir'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        default=None,
        help='Directorio de salida (por defecto: misma ubicación que el archivo de entrada)'
    )
    
    parser.add_argument(
        '-f', '--format',
        dest='format',
        choices=['png', 'jpeg', 'jpg'],
        default='png',
        help='Formato de salida (por defecto: png)'
    )
    
    parser.add_argument(
        '-s', '--scale',
        dest='scale',
        type=float,
        default=1.0,
        help='Factor de escala para el tamaño de salida (por defecto: 1.0)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        dest='quality',
        type=int,
        default=95,
        help='Calidad para JPEG (1-100, por defecto: 95)'
    )
    
    args = parser.parse_args()
    
    # Validar calidad
    if not 1 <= args.quality <= 100:
        print("Error: La calidad debe estar entre 1 y 100")
        sys.exit(1)
    
    # Validar escala
    if args.scale <= 0:
        print("Error: El factor de escala debe ser mayor que 0")
        sys.exit(1)
    
    # Normalizar formato
    output_format = 'jpeg' if args.format in ('jpeg', 'jpg') else 'png'
    
    # Procesar archivos
    process_files(
        args.input_files,
        args.output_dir,
        output_format,
        args.scale,
        args.quality
    )


if __name__ == '__main__':
    main()
