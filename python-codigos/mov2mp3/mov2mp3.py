#!/usr/bin/env python3
import sys
import os
import argparse
import ffmpeg

def convertir_video_a_mp3(entrada, salida, bitrate="192k", fps=44100, overwrite=False, verbose=True):
    if not os.path.exists(entrada):
        raise FileNotFoundError(f"El archivo de entrada no existe: {entrada}")

    if not salida.lower().endswith(".mp3"):
        raise ValueError("El archivo de salida debe terminar en .mp3")

    try:
        # Comprueba si hay una pista de audio antes de convertir
        try:
            probe = ffmpeg.probe(entrada)
            audio_streams = [s for s in probe['streams'] if s['codec_type'] == 'audio']
            if not audio_streams:
                raise RuntimeError("El video no contiene pista de audio.")
        except ffmpeg.Error as e:
            stderr = e.stderr.decode('utf8') if e.stderr else "No stderr"
            raise RuntimeError(f"No se pudo analizar el archivo de entrada: {stderr}") from e

        stream = ffmpeg.input(entrada)
        # Selecciona solo la pista de audio para procesar
        stream = stream.audio
        stream = ffmpeg.output(stream, salida, audio_bitrate=bitrate, ar=fps, acodec='libmp3lame')
        stream.run(quiet=(not verbose), overwrite_output=overwrite)

    except ffmpeg.Error as e:
        stderr = e.stderr.decode('utf8') if e.stderr else "No stderr"
        raise RuntimeError(f"Error durante la conversión con ffmpeg: {stderr}") from e

def ruta_salida_por_defecto(entrada):
    base, _ = os.path.splitext(entrada)
    return base + ".mp3"

def main():
    parser = argparse.ArgumentParser(
        description="Convierte archivos de video (.mov, .mp4) a .mp3 usando ffmpeg-python."
    )
    parser.add_argument("entrada", help="Ruta al archivo de video o directorio de entrada")
    parser.add_argument("salida", nargs="?", help="Ruta de salida .mp3 (para un solo archivo) o directorio de salida (para un directorio de entrada). Opcional.")
    parser.add_argument("--bitrate", default="192k", help="Bitrate de salida (ej: 128k, 192k, 256k)")
    parser.add_argument("--fps", type=int, default=44100, help="Sample rate (ej: 44100, 48000)")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir si el archivo de salida existe")
    parser.add_argument("--quiet", action="store_true", help="No mostrar logs de ffmpeg")
    args = parser.parse_args()

    entrada = args.entrada
    salida_arg = args.salida

    try:
        if os.path.isdir(entrada):
            # Procesar un directorio
            files_to_process = [f for f in os.listdir(entrada) if f.lower().endswith(('.mov', '.mp4'))]
            if not files_to_process:
                print(f"No se encontraron archivos .mov o .mp4 en '{entrada}'.")
                return

            print(f"Se encontraron {len(files_to_process)} archivos para convertir en '{entrada}'.")

            output_dir = salida_arg
            if output_dir:
                if not os.path.isdir(output_dir):
                    if os.path.exists(output_dir):
                        raise ValueError("La ruta de salida especificada existe pero no es un directorio.")
                    os.makedirs(output_dir)
            else:
                output_dir = entrada # Salida en el mismo directorio de entrada

            for filename in files_to_process:
                input_path = os.path.join(entrada, filename)
                output_filename = os.path.splitext(filename)[0] + ".mp3"
                output_path = os.path.join(output_dir, output_filename)

                try:
                    print(f"\nConvirtiendo '{input_path}'...")
                    convertir_video_a_mp3(
                        entrada=input_path,
                        salida=output_path,
                        bitrate=args.bitrate,
                        fps=args.fps,
                        overwrite=args.overwrite,
                        verbose=not args.quiet
                    )
                    print(f"✅ Conversión completada: {output_path}")
                except (FileExistsError, Exception) as e:
                    print(f"⚠️  Error al convertir '{input_path}': {e}")
                    # No salimos, continuamos con el siguiente archivo

        elif os.path.isfile(entrada):
            # Procesar un solo archivo
            if not entrada.lower().endswith(('.mov', '.mp4')):
                raise ValueError("El archivo de entrada debe ser de tipo .mov o .mp4")

            salida = salida_arg or ruta_salida_por_defecto(entrada)

            convertir_video_a_mp3(
                entrada=entrada,
                salida=salida,
                bitrate=args.bitrate,
                fps=args.fps,
                overwrite=args.overwrite,
                verbose=not args.quiet
            )
            print(f"✅ Conversión completada: {salida}")
        else:
            raise FileNotFoundError(f"La ruta de entrada no existe o no es un archivo/directorio válido: {entrada}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
