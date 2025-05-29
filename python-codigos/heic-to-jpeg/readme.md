# HEIC a JPEG

## Descripción

Este proyecto proporciona un script en Python que convierte imágenes en formato HEIC a JPEG, corrige su orientación basada en metadatos EXIF y aplica compresión ajustable de calidad. Utiliza la utilidad `sips` en macOS y la biblioteca Pillow para la manipulación de imágenes.

## Instalación

1. **Requisitos previos**:

   * macOS con la herramienta `sips` disponible.
   * Python 3.6 o superior.

2. **Clonar el repositorio**:

   ```bash
   git clone https://tu-repositorio.git
   cd tu-repositorio
   ```

3. **Crear y activar un entorno virtual (opcional pero recomendado)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

4. **Instalar dependencias**:

   ```bash
   pip install Pillow
   ```

## Uso

1. **Preparar directorios**:

   * Coloca tus archivos `.heic` en la carpeta `./input`.
   * El script creará la carpeta `./output` si no existe.

2. **Ejecutar el script**:

   ```bash
   python heic_to_jpeg.py
   ```

   Por defecto, el script usa calidad de compresión `70`. Puedes modificar esta variable directamente en el código o pasar un parámetro si lo adaptas.

## Opciones o configuración

* **`input_dir`**: Ruta al directorio de entrada con archivos `.heic`. Por defecto `./input`.
* **`output_dir`**: Ruta donde se guardarán los `.jpeg` convertidos. Por defecto `./output`.
* **`calidad`**: Calidad de compresión JPEG (1–95). Se define en la variable `calidad_compresion` del script (por defecto `70`).

---

*Generado automáticamente.*