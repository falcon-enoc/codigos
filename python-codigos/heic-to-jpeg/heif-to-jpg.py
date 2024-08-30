import os
import subprocess
from PIL import Image, ExifTags

def corregir_orientacion(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(orientation, 1)

            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # Casos en los que la imagen no tiene información EXIF
        pass

    return img

def heic_to_jpeg(input_dir, output_dir, calidad=85):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.heic'):
            heic_file_path = os.path.join(input_dir, filename)
            jpeg_file_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}.jpeg')

            # Comando sips para convertir .heic a .jpeg
            try:
                subprocess.run(["sips", "-s", "format", "jpeg", heic_file_path, "--out", jpeg_file_path], check=True)
                print(f"Convertido: {filename} -> {os.path.basename(jpeg_file_path)}")

                # Abrir el archivo JPEG, corregir la orientación y comprimirlo
                with Image.open(jpeg_file_path) as img:
                    img = corregir_orientacion(img)
                    img.save(jpeg_file_path, "JPEG", quality=calidad)
                    print(f"Imagen comprimida: {jpeg_file_path} con calidad {calidad}")

            except subprocess.CalledProcessError as e:
                print(f"Error al convertir {filename}: {e}")

input_directory = "./input"
output_directory = "./output"
calidad_compresion = 70  # Ajusta este valor entre 1 (baja calidad) y 95 (alta calidad)

heic_to_jpeg(input_directory, output_directory, calidad=calidad_compresion)
