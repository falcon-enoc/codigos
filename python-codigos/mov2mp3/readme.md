# 🎵 Conversor de Video (.MOV, .MP4) a .MP3 con Python y ffmpeg

Este script permite **extraer el audio de archivos de video (`.mov`, `.mp4`)** y guardarlo en formato `.mp3`.
Funciona usando la librería [ffmpeg-python](https://github.com/kkroening/ffmpeg-python), que es una envoltura de Python para `ffmpeg`.

---

## 🚀 Requisitos

- Python **3.7 o superior**
- La herramienta de línea de comandos **`ffmpeg`**.
- Librería **`ffmpeg-python`**

### Instalación de `ffmpeg`

Antes de usar el script, debes tener `ffmpeg` instalado en tu sistema y accesible desde la línea de comandos (en tu PATH).

-   **En macOS (usando [Homebrew](https://brew.sh/)):**
    ```bash
    brew install ffmpeg
    ```
-   **En Windows (usando [Chocolatey](https://chocolatey.org/)):**
    ```bash
    choco install ffmpeg
    ```
-   **En Linux (usando `apt`):**
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```

### Instalación de la librería de Python

```bash
pip install ffmpeg-python
```

## 💡 Uso

El script puede procesar un solo archivo de video o todos los archivos de video (`.mov`, `.mp4`) dentro de un directorio.

### Convertir un solo archivo

```bash
python mov2mp3.py <ruta_al_archivo_de_entrada> [ruta_de_salida.mp3] [opciones]
```

-   `<ruta_al_archivo_de_entrada>`: Ruta al archivo de video (`.mov` o `.mp4`) que deseas convertir.
-   `[ruta_de_salida.mp3]` (opcional): Ruta y nombre del archivo MP3 de salida. Si no se especifica, se creará un archivo MP3 con el mismo nombre y en la misma ubicación que el archivo de entrada.

Ejemplo:
```bash
python mov2mp3.py mi_video.mp4 mi_audio.mp3
python mov2mp3.py otro_video.mov
```

### Convertir todos los archivos en un directorio

```bash
python mov2mp3.py <ruta_al_directorio_de_entrada> [ruta_al_directorio_de_salida] [opciones]
```

-   `<ruta_al_directorio_de_entrada>`: Ruta al directorio que contiene los archivos de video (`.mov` o `.mp4`) a convertir.
-   `[ruta_al_directorio_de_salida]` (opcional): Ruta al directorio donde se guardarán los archivos MP3 convertidos. Si no se especifica, los archivos MP3 se crearán en el mismo directorio que los archivos de entrada.

Ejemplo:
```bash
python mov2mp3.py videos/ audios_convertidos/
python mov2mp3.py mis_grabaciones/
```

### Opciones

-   `--bitrate <valor>`: Bitrate de salida para el MP3 (ej: `128k`, `192k`, `256k`). Por defecto es `192k`.
-   `--fps <valor>`: Sample rate (frecuencia de muestreo) para el audio (ej: `44100`, `48000`). Por defecto es `44100`.
-   `--overwrite`: Sobrescribe el archivo de salida si ya existe.
-   `--quiet`: No muestra la barra de progreso durante la conversión.
