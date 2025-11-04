#!/usr/bin/env python3
import sys
import os
import argparse
import moviepy as mp

def convertir_mov_a_mp3(entrada, salida, bitrate="192k", fps=44100, overwrite=False, verbose=True):
    if not os.path.exists(entrada):
        raise FileNotFoundError(f"El archivo de entrada no existe: {entrada}")

    if not salida.lower().endswith(".mp3"):
        raise ValueError("El archivo de salida debe terminar en .mp3")

    if os.path.exists(salida) and not overwrite:
        raise FileExistsError(f"El archivo de salida ya existe: {salida}. Usa --overwrite para reemplazarlo.")

    # Carga y extrae audio
    clip = mp.VideoFileClip(entrada)
    try:
        if clip.audio is None:
            raise RuntimeError("El video no contiene pista de audio.")
        # Desactiva el logger de moviepy si no quieres progreso en consola
        logger = None if not verbose else "bar"
        clip.audio.write_audiofile(
            salida,
            bitrate=bitrate,   # calidad/bitrate de mp3
            fps=fps,           # sample rate
            logger=logger
        )
    finally:
        # Cierra recursos (muy importante en Windows)
        clip.close()
        if clip.audio:
            clip.audio.close()

def ruta_salida_por_defecto(entrada):
    base, _ = os.path.splitext(entrada)
    return base + ".mp3"

def main():
    parser = argparse.ArgumentParser(
        description="Convierte un archivo .mov a .mp3 usando MoviePy."
    )
    parser.add_argument("entrada", help="Ruta al archivo .mov de entrada")
    parser.add_argument("salida", nargs="?", help="Ruta de salida .mp3 (opcional)")
    parser.add_argument("--bitrate", default="192k", help="Bitrate de salida (ej: 128k, 192k, 256k)")
    parser.add_argument("--fps", type=int, default=44100, help="Sample rate (ej: 44100, 48000)")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir si el archivo de salida existe")
    parser.add_argument("--quiet", action="store_true", help="No mostrar barra de progreso")
    args = parser.parse_args()

    entrada = args.entrada
    salida = args.salida or ruta_salida_por_defecto(entrada)

    try:
        convertir_mov_a_mp3(
            entrada=entrada,
            salida=salida,
            bitrate=args.bitrate,
            fps=args.fps,
            overwrite=args.overwrite,
            verbose=not args.quiet
        )
        print(f"✅ Conversión completada: {salida}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
