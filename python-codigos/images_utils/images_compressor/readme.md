# Compresor de Imágenes

Un script en Python para comprimir imágenes reduciendo su tamaño de archivo mientras mantiene la calidad visual. Soporta procesamiento de archivos individuales y directorios completos.

## Características

- ✅ **Múltiples formatos**: JPG, PNG, BMP, TIFF, WebP, HEIC/HEIF
- ✅ **Compresión inteligente**: Optimiza automáticamente para reducir tamaño
- ✅ **Redimensionamiento opcional**: Controla las dimensiones máximas
- ✅ **Procesamiento por lotes**: Procesa directorios completos
- ✅ **Corrección automática**: Corrige orientación EXIF
- ✅ **Estadísticas detalladas**: Muestra ahorro de espacio
- ✅ **Manejo de transparencias**: Convierte PNG con transparencia a JPG

## Instalación

### Prerrequisitos

El script requiere Python 3.6+ y las siguientes dependencias:

```bash
pip install Pillow pillow-heif
```

### Descarga

1. Descarga el archivo `image_compressor.py`
2. Hazlo ejecutable (Linux/Mac):
   ```bash
   chmod +x image_compressor.py
   ```

## Uso

### Sintaxis básica

```bash
python3 image_compressor.py <entrada> -o <salida> [opciones]
```

### Parámetros

| Parámetro | Descripción | Requerido |
|-----------|-------------|-----------|
| `entrada` | Archivo de imagen o directorio | ✅ |
| `-o`, `--output` | Directorio de salida | ✅ |
| `-q`, `--quality` | Calidad de compresión (1-100) | ❌ (default: 85) |
| `--max-width` | Ancho máximo en píxeles | ❌ |
| `--max-height` | Alto máximo en píxeles | ❌ |
| `--suffix` | Sufijo para archivos comprimidos | ❌ (default: _compressed) |

### Ejemplos de uso

#### 1. Comprimir una imagen individual

```bash
python3 image_compressor.py foto.jpg -o compressed/
```

#### 2. Comprimir con calidad personalizada

```bash
python3 image_compressor.py imagen.png -o output/ -q 90
```

#### 3. Comprimir directorio completo

```bash
python3 image_compressor.py fotos/ -o compressed/ -q 80
```

#### 4. Redimensionar y comprimir

```bash
python3 image_compressor.py imagen.jpg -o output/ --max-width 1920 --max-height 1080
```

#### 5. Procesamiento completo con configuración personalizada

```bash
python3 image_compressor.py photos/ -o compressed/ -q 75 --max-width 1920 --suffix _optimized
```

## Formatos soportados

### Entrada
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **BMP** (.bmp)
- **TIFF** (.tiff, .tif)
- **WebP** (.webp)
- **HEIC/HEIF** (.heic, .heif)

### Salida
- **JPEG** (.jpg) - Todos los archivos se convierten a JPEG para máxima compatibilidad y compresión

## Cómo funciona

### Proceso de compresión

1. **Carga de imagen**: Abre la imagen usando Pillow
2. **Corrección EXIF**: Corrige la orientación automáticamente
3. **Conversión de formato**: Convierte a RGB si es necesario
4. **Manejo de transparencias**: Coloca fondo blanco en PNG transparentes
5. **Redimensionamiento**: Reduce dimensiones si se especifica
6. **Optimización**: Aplica compresión JPEG optimizada
7. **Guardado**: Guarda con la calidad especificada

### Algoritmo de calidad

El script usa compresión JPEG con optimización automática:
- **Quality 95-100**: Calidad máxima, compresión mínima
- **Quality 85-94**: Calidad alta, buen balance
- **Quality 75-84**: Calidad media, buena compresión
- **Quality 60-74**: Calidad aceptable, alta compresión
- **Quality <60**: Calidad baja, máxima compresión

## Estructura del código

### Funciones principales

#### `compress_image(input_path, output_path, quality, max_width, max_height)`
Comprime una imagen individual con los parámetros especificados.

**Parámetros:**
- `input_path`: Ruta de la imagen original
- `output_path`: Ruta donde guardar la imagen comprimida
- `quality`: Calidad de compresión (1-100)
- `max_width`: Ancho máximo opcional
- `max_height`: Alto máximo opcional

**Retorna:**
- Tupla con (tamaño_original, tamaño_comprimido, porcentaje_reducción)

#### `process_images(input_path, output_dir, quality, max_width, max_height, suffix)`
Procesa múltiples imágenes desde un archivo o directorio.

#### `format_size(size_bytes)`
Convierte bytes a unidades legibles (B, KB, MB, GB).

### Manejo de errores

- Valida formatos de archivo soportados
- Verifica que las rutas existan
- Maneja errores de lectura/escritura
- Muestra mensajes informativos de progreso

## Consejos de uso

### Calidad recomendada por uso

- **Fotografías para web**: 80-85
- **Imágenes para redes sociales**: 75-80
- **Archivos para almacenamiento**: 85-90
- **Compresión máxima**: 60-70

### Redimensionamiento

Para reducir significativamente el tamaño:
- **Full HD**: `--max-width 1920 --max-height 1080`
- **HD**: `--max-width 1280 --max-height 720`
- **Redes sociales**: `--max-width 1080 --max-height 1080`

### Estructura de salida

```
output/
├── imagen1_compressed.jpg
├── imagen2_compressed.jpg
└── subdirectorio/
    ├── imagen3_compressed.jpg
    └── imagen4_compressed.jpg
```

## Solución de problemas

### Error: "No module named 'PIL'"

```bash
pip install Pillow
```

### Error: "No module named 'pillow_heif'"

```bash
pip install pillow-heif
```

### Error: "Permission denied"

Verifica permisos de escritura en el directorio de salida:

```bash
chmod 755 output_directory/
```

### Imágenes muy grandes

Para archivos muy grandes, usa redimensionamiento:

```bash
python3 image_compressor.py imagen.jpg -o output/ --max-width 1920 -q 80
```

## Contribuir

Para mejorar este script:

1. Haz un fork del proyecto
2. Crea una rama para tu característica
3. Realiza tus cambios
4. Envía un pull request

## Licencia

Este script está disponible bajo la licencia MIT. Úsalo libremente en tus proyectos.

---

**Nota**: Este script está optimizado para uso general. Para casos específicos (como imágenes médicas o científicas), considera ajustar los parámetros de calidad.