#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import subprocess
from pathlib import Path

POWERSCRIPT = r'''
on run argv
    if (count of argv) is not 2 then
        error "Se esperaban 2 argumentos: inPath outPath"
    end if
    set inPosix to item 1 of argv
    set outPosix to item 2 of argv

    set inFile to POSIX file inPosix
    set outFile to POSIX file outPosix

    tell application "Microsoft PowerPoint"
        -- Abrir la presentación (no muestra UI si se invoca vía osascript)
        set thePres to open inFile

        -- Guardar como PDF
        -- Sintaxis AppleScript para PowerPoint macOS:
        -- save as <presentation> <file> file format save as PDF
        save as thePres outFile file format save as PDF

        -- Cerrar sin guardar cambios en el PPTX original
        close thePres saving no
    end tell
end run
'''

def keynote_escape_path(p: Path) -> str:
    # osascript usa POSIX paths; aseguramos string absoluto
    return str(p.resolve())

def convert_one(inpath: Path, outdir: Path, overwrite: bool = False):
    if not inpath.exists():
        raise FileNotFoundError(f"No existe: {inpath}")

    if inpath.suffix.lower() != ".pptx":
        raise ValueError(f"No es .pptx: {inpath}")

    outdir.mkdir(parents=True, exist_ok=True)
    outpdf = outdir / (inpath.stem + ".pdf")

    if outpdf.exists() and not overwrite:
        print(f"⚠️  Ya existe, omito (usa --overwrite): {outpdf}")
        return outpdf

    cmd = ["osascript", "-e", POWERSCRIPT, keynote_escape_path(inpath), keynote_escape_path(outpdf)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ PDF generado: {outpdf}")
        return outpdf
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", errors="ignore")
        out = e.stdout.decode("utf-8", errors="ignore")
        raise RuntimeError(f"Fallo al exportar {inpath}:\nSTDOUT:\n{out}\nSTDERR:\n{err}") from e

def walk_and_convert(indir: Path, outdir: Path, recursive: bool, overwrite: bool):
    pattern = "**/*.pptx" if recursive else "*.pptx"
    files = sorted(indir.glob(pattern))
    if not files:
        print(f"(i) No se encontraron .pptx en {indir} (recursive={recursive})")
        return
    for f in files:
        # Si se procesa recursivo, replicar estructura en salida
        rel = f.relative_to(indir) if recursive else Path(f.name)
        target_dir = outdir / rel.parent
        try:
            convert_one(f, target_dir, overwrite=overwrite)
        except Exception as ex:
            print(f"❌ Error con {f} → {ex}")

def main():
    ap = argparse.ArgumentParser(
        description="Exporta PPTX a PDF usando Microsoft PowerPoint (macOS) sin interfaz."
    )
    ap.add_argument("input", help="Archivo .pptx o carpeta con .pptx")
    ap.add_argument("-o", "--output", help="Carpeta de salida. Por defecto: misma carpeta (archivo) o <input>/pdf (carpeta)")
    ap.add_argument("-r", "--recursive", action="store_true", help="Recorrer subcarpetas (si input es carpeta)")
    ap.add_argument("--overwrite", action="store_true", help="Sobrescribir PDFs existentes")
    args = ap.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"No existe la ruta: {input_path}")
        sys.exit(1)

    if input_path.is_file():
        if input_path.suffix.lower() != ".pptx":
            print("El input debe ser .pptx o una carpeta.")
            sys.exit(1)
        outdir = Path(args.output).expanduser().resolve() if args.output else input_path.parent
        try:
            convert_one(input_path, outdir, overwrite=args.overwrite)
        except Exception as ex:
            print(f"❌ Error: {ex}")
            sys.exit(2)
    else:
        # Carpeta
        default_out = input_path / "pdf"
        outdir = Path(args.output).expanduser().resolve() if args.output else default_out
        walk_and_convert(input_path, outdir, recursive=args.recursive, overwrite=args.overwrite)

if __name__ == "__main__":
    main()

