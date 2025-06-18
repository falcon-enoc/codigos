# PDF Splitter

Una herramienta de línea de comandos para separar archivos PDF en segmentos específicos de páginas.

## 📋 Descripción

PDF Splitter permite extraer páginas específicas o rangos de páginas de un archivo PDF y crear nuevos archivos PDF independientes. Es útil para dividir documentos largos, extraer capítulos específicos, o crear versiones más pequeñas de documentos PDF.

## 🚀 Instalación

### Requisitos previos
- Python 3.6 o superior
- pip (gestor de paquetes de Python)

### Instalar dependencias

```bash
pip install -r requirements.txt
```

O instalar directamente:

```bash
pip install PyPDF2
```

## 💻 Uso

### Sintaxis básica

```bash
python spliter.py <archivo.pdf> -s <segmentos> [opciones]
```

### Parámetros

- `archivo.pdf`: Archivo PDF de entrada (obligatorio)
- `-s, --segmentos`: Segmentos a extraer (obligatorio)
- `-o, --output-dir`: Directorio de salida (opcional)
- `-v, --verbose`: Mostrar información detallada (opcional)
- `-h, --help`: Mostrar ayuda

## 📝 Formatos de segmentos

El script soporta varios formatos para especificar los segmentos:

| Formato | Descripción | Ejemplo |
|---------|-------------|---------|
| `"5"` | Solo la página 5 | `"3"` |
| `"1-5"` | Páginas 1 a 5 | `"10-15"` |
| `"10-"` | Desde página 10 hasta el final | `"20-"` |
| `"-5"` | Desde el inicio hasta página 5 | `"-10"` |

## 🔧 Ejemplos de uso

### Ejemplo 1: Extraer páginas individuales
```bash
python spliter.py documento.pdf -s "1" "5" "10"
```
Crea tres archivos:
- `documento_pagina_1.pdf`
- `documento_pagina_5.pdf`
- `documento_pagina_10.pdf`

### Ejemplo 2: Extraer rangos de páginas
```bash
python spliter.py manual.pdf -s "1-5" "10-15" "20-25"
```
Crea tres archivos:
- `manual_paginas_1-5.pdf`
- `manual_paginas_10-15.pdf`
- `manual_paginas_20-25.pdf`

### Ejemplo 3: Combinar formatos
```bash
python spliter.py libro.pdf -s "1-3" "7" "10-" "-5"
```
Extrae:
- Páginas 1 a 3
- Solo la página 7
- Desde página 10 hasta el final
- Desde el inicio hasta página 5

### Ejemplo 4: Especificar directorio de salida
```bash
python spliter.py documento.pdf -s "1-10" "20-30" --output-dir salida/
```
Guarda los archivos en el directorio `salida/`

### Ejemplo 5: Modo verbose
```bash
python spliter.py archivo.pdf -s "1-5" "10-15" --verbose
```
Muestra información detallada del proceso

## 📁 Archivos de salida

Los archivos generados siguen este patrón de nomenclatura:

- **Página individual**: `{nombre_original}_pagina_{numero}.pdf`
- **Rango de páginas**: `{nombre_original}_paginas_{inicio}-{fin}.pdf`

### Ejemplo:
Si el archivo original es `manual_usuario.pdf` y extraes las páginas 1-5:
- Archivo generado: `manual_usuario_paginas_1-5.pdf`

## ⚠️ Manejo de errores

El script maneja varios tipos de errores:

- **Archivo no encontrado**: Verifica que el archivo PDF existe
- **Formato inválido**: Valida que el archivo sea un PDF válido
- **Páginas fuera de rango**: Comprueba que los números de página estén dentro del documento
- **Formato de segmento incorrecto**: Valida la sintaxis de los segmentos

### Mensajes de error comunes:

```
❌ Error: El archivo documento.pdf no existe
❌ Error: Página 100 fuera de rango (1-50)
❌ Error: Formato de página inválido: abc
❌ Error: Rango inválido: 10-5 (total páginas: 20)
```

## 🛠️ Funcionalidades

### ✅ Características implementadas:
- Extracción de páginas individuales
- Extracción de rangos de páginas
- Rangos abiertos (desde/hasta el final)
- Validación de archivos PDF
- Validación de rangos de páginas
- Creación automática de directorios
- Nomenclatura intuitiva de archivos
- Manejo robusto de errores
- Interfaz de línea de comandos completa

### 🔄 Flujo de trabajo:
1. Validación del archivo PDF de entrada
2. Análisis de los segmentos especificados
3. Validación de rangos de páginas
4. Extracción y creación de archivos PDF
5. Reporte de resultados

## 🏗️ Estructura del código

```
spliter.py
├── validar_archivo_pdf()     # Validación de archivos PDF
├── parsear_segmento()        # Análisis de formatos de segmentos
├── crear_pdf_segmento()      # Creación de archivos PDF
├── separar_pdf()             # Función principal de separación
└── main()                    # Interfaz de línea de comandos
```

## 🐛 Solución de problemas

### Problema: "PyPDF2 no está instalado"
**Solución:**
```bash
pip install PyPDF2
```

### Problema: "Archivo no encontrado"
**Solución:**
- Verifica la ruta del archivo
- Asegúrate de que el archivo existe
- Usa rutas absolutas si es necesario

### Problema: "Error al leer el PDF"
**Solución:**
- Verifica que el archivo no esté corrupto
- Asegúrate de que es un PDF válido
- Intenta abrir el archivo en un visor de PDF

## 📊 Ejemplos avanzados

### Dividir un documento por capítulos:
```bash
python spliter.py tesis.pdf -s "1-10" "11-25" "26-40" "41-60" --output-dir capitulos/
```

### Extraer solo las páginas impares:
```bash
python spliter.py documento.pdf -s "1" "3" "5" "7" "9" "11" "13" "15"
```

### Crear respaldo de secciones específicas:
```bash
python spliter.py manual.pdf -s "1-5" "50-55" "100-" --output-dir backup/
```

## 🤝 Contribuciones

Si encuentras bugs o tienes sugerencias de mejora, no dudes en:
1. Reportar issues
2. Sugerir nuevas funcionalidades
3. Enviar pull requests

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Nota**: Asegúrate de tener los permisos necesarios para leer el archivo PDF de entrada y escribir en el directorio de salida.
