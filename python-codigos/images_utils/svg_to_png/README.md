# SVG to PNG/JPEG Converter

Script en Python para convertir imágenes SVG a formatos PNG o JPEG con opciones avanzadas de configuración.

## 🚀 Características

- ✅ Conversión de SVG a PNG o JPEG
- ✅ Soporte para múltiples archivos simultáneos
- ✅ Control de escala de salida
- ✅ Control de calidad para JPEG
- ✅ Salida personalizable con flag `-o`
- ✅ Por defecto guarda en la misma ubicación del archivo original
- ✅ Interfaz de línea de comandos intuitiva
- ✅ Manejo de transparencias (convierte a fondo blanco en JPEG)

## 📋 Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
```bash
cd images_utils/svg_to_png
```

3. Instala las dependencias:

**Opción 1: Usando pyproject.toml (moderna - recomendada)**
```bash
pip install .
```

### Instalación en macOS

Si tienes problemas instalando `cairosvg`, primero instala las dependencias del sistema:

```bash
brew install cairo pkg-config
brew install librsvg   # para el backend alternativo rsvg-convert
pip install .
```

### Instalación en Linux (Ubuntu/Debian)

```bash
sudo apt-get install libcairo2-dev pkg-config python3-dev
sudo apt-get install librsvg2-bin   # para rsvg-convert
pip install .
```

### Instalación en Windows

Descarga e instala GTK+ desde: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

Luego instala las dependencias de Python:
```bash
pip install .
```

## 💻 Uso

### Sintaxis básica

```bash
python svg_converter.py [archivos] [opciones]
```

### Opciones disponibles

- `-h, --help`: Muestra la ayuda y ejemplos de uso
- `-o, --output DIRECTORIO`: Especifica el directorio de salida (por defecto: misma ubicación del archivo)
- `-f, --format FORMATO`: Formato de salida: `png`, `jpeg` o `jpg` (por defecto: `png`)
- `-s, --scale ESCALA`: Factor de escala (por defecto: `1.0`)
- `-q, --quality CALIDAD`: Calidad JPEG de 1 a 100 (por defecto: `95`)
- `--backend {auto,cairosvg,rsvg}`: Selecciona el motor de conversión. `auto` intenta CairoSVG y, si falla, usa `rsvg-convert`.
- `--skip-validation`: Omite la validación XML del SVG (útil si `rsvg-convert` tolera archivos mal formados).

### Ejemplos de uso

#### Convertir un solo archivo a PNG (misma ubicación)
```bash
python svg_converter.py imagen.svg
```

#### Convertir múltiples archivos
```bash
python svg_converter.py imagen1.svg imagen2.svg imagen3.svg
```

#### Convertir todos los SVG del directorio actual
```bash
python svg_converter.py *.svg
```

#### Especificar directorio de salida
```bash
python svg_converter.py imagen.svg -o ./salida
```

#### Convertir a JPEG
```bash
python svg_converter.py imagen.svg -f jpeg
```

#### Usar backend alternativo rsvg (más tolerante)
```bash
python svg_converter.py imagen.svg --backend rsvg
# o con el entrypoint instalado
svg-converter imagen.svg --backend rsvg
```

#### Omitir validación XML (si conoces el archivo y usas rsvg)
```bash
svg-converter imagen.svg --backend rsvg --skip-validation
```

#### Convertir con mayor escala (imagen más grande)
```bash
python svg_converter.py imagen.svg -s 2.0
```

#### Convertir a JPEG con calidad específica
```bash
python svg_converter.py imagen.svg -f jpeg -q 90 -o ./salida
```

#### Combinar todas las opciones
```bash
python svg_converter.py *.svg -f jpeg -s 1.5 -q 85 -o ./imagenes_convertidas
```

## 📁 Estructura de salida

Por defecto, los archivos convertidos se guardan en la misma ubicación que los archivos originales:

```
/ruta/original/
  ├── imagen.svg
  └── imagen.png  (generado)
```

Con la opción `-o`, puedes especificar un directorio diferente:

```
/ruta/original/
  └── imagen.svg

/ruta/salida/
  └── imagen.png  (generado con -o /ruta/salida)
```

## 🎨 Características técnicas

### Conversión a PNG
- Mantiene la transparencia del SVG original
- Soporte para escala personalizada
- Alta calidad de renderizado usando Cairo

### Conversión a JPEG
- Convierte transparencias a fondo blanco
- Control de calidad de compresión (1-100)
- Optimizado para web y compartir

### Factor de escala
- `1.0`: Tamaño original
- `2.0`: Doble de tamaño (ideal para pantallas Retina)
- `0.5`: Mitad del tamaño (para miniaturas)

## 🐛 Solución de problemas

### Error: "No module named 'cairosvg'"
Ejecuta:
```bash
pip install .
```

O si prefieres usar requirements.txt:
```bash
pip install -r requirements.txt
```

### Error en macOS: "cairo not found"
Instala Cairo con Homebrew:
```bash
brew install cairo pkg-config
pip install --upgrade --force-reinstall cairosvg
```

### Error: "Permission denied"
Dale permisos de ejecución al script:
```bash
chmod +x svg_converter.py
```

## 📝 Notas

- Los archivos SVG deben tener extensión `.svg`
- El formato JPEG no soporta transparencias (se convierte a fondo blanco)
- Para imágenes con transparencia, se recomienda usar PNG
- Las imágenes de salida mantienen el mismo nombre base que el archivo original

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz un fork del proyecto
2. Crea una rama para tu característica
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ✨ Autor

Creado con ❤️ para facilitar la conversión de imágenes SVG.

## 📚 Recursos adicionales

- [Documentación de CairoSVG](https://cairosvg.org/)
- [Documentación de Pillow](https://pillow.readthedocs.io/)
- [Especificación SVG](https://www.w3.org/TR/SVG2/)
