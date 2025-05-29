# Conversor de Imágenes a PDF

## Descripción

Este script de Python convierte todas las imágenes de una carpeta en un documento PDF, colocando cada imagen en una página individual. Cada página incluye el nombre del archivo de la imagen como título en la parte superior.

## Requisitos

- Python 3.x
- Bibliotecas requeridas:
  - PIL (Pillow): Para el procesamiento de imágenes
  - reportlab: Para la generación de PDFs

Puedes instalar las dependencias con:

```bash
pip3 install pillow reportlab
```

## Preparación de datos

Antes de ejecutar el programa, asegúrate de:

1. Tener todas las imágenes que deseas convertir en una sola carpeta
2. Los formatos de imagen soportados son:
   - JPG/JPEG
   - PNG
   - GIF
   - BMP
   - TIFF
3. Las imágenes se ordenarán alfabéticamente por nombre de archivo en el PDF resultante
4. Si deseas un orden específico, puedes renombrar tus archivos con prefijos numéricos (ej: 01_imagen.jpg, 02_imagen.jpg, etc.)

## Ejecución

**IMPORTANTE**: Las rutas de carpetas y archivos SIEMPRE deben ir entre comillas dobles ("") para evitar problemas con espacios o caracteres especiales.

Hay dos formas de ejecutar el programa:

### 1. Especificando la ruta de salida del PDF

```bash
python3 images_to_pdf.py "/ruta/a/carpeta/imagenes" -o "/ruta/salida.pdf"
```

### 2. Usando el directorio actual para guardar el PDF

```bash
python3 images_to_pdf.py "/ruta/a/carpeta/imagenes"
```

En este caso, el PDF se guardará en el directorio donde se ejecuta el script, usando el nombre de la carpeta de imágenes como nombre del archivo PDF.

## Ejemplos

1. Convertir imágenes de la carpeta "Vacaciones" y guardar el PDF en el escritorio:

```bash
python3 images_to_pdf.py "~/Imágenes/Vacaciones" -o "~/Desktop/vacaciones.pdf"
```

2. Convertir imágenes de la carpeta "Documentos" y guardar el PDF en el directorio actual:

```bash
python3 images_to_pdf.py "~/Imágenes/Documentos"
```

Esto creará un archivo "Documentos.pdf" en el directorio donde se ejecutó el comando.

## Características adicionales

- El tamaño de cada página del PDF se ajusta automáticamente al tamaño de la imagen correspondiente
- Se añade un margen superior para el título de la imagen (nombre del archivo)
- Si no se encuentran imágenes en la carpeta especificada, el programa mostrará un mensaje y no creará ningún PDF

## Solución de problemas

- Si el programa muestra un error de importación, asegúrate de haber instalado las bibliotecas requeridas
- Si no se encuentran imágenes, verifica que la carpeta contenga archivos con las extensiones soportadas
- Si el PDF resultante está vacío o incompleto, verifica que tengas permisos de escritura en el directorio de salida
- Si recibes errores relacionados con la ruta, asegúrate de que todas las rutas estén entre comillas dobles ("") y sean correctas


## Posbiles integraciones futuras
[] Añadir rotacion automatica de las images