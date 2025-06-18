# Analizador de Archivos de Texto

## Descripción

Este script en Python analiza un archivo de texto y proporciona información básica sobre él: número de líneas, número de palabras y número de caracteres. Opcionalmente, permite al usuario imprimir un rango específico de líneas mediante argumentos de línea de comandos.

## Instalación

1. Asegúrate de tener Python 3.6 o superior instalado.
2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. No requiere librerías externas adicionales.

## Uso

Ejecuta el script indicando la ruta al archivo de texto y, si lo deseas, un rango de líneas:

```bash
python info_txt.py <file_path> [line_range]
```

* `<file_path>`: Ruta al archivo de texto a analizar.
* `[line_range]`: (Opcional) Rango de líneas a imprimir. Formatos admitidos:

  * `N` imprime solo la línea N.
  * `M:N` imprime desde la línea M hasta la línea N.
  * `:N` imprime desde la línea 1 hasta N.
  * `M:` imprime desde la línea M hasta el final.

### Ejemplos

* Obtener solo información básica:

  ```bash
  python info_txt.py documento.txt
  # Salida: {'Numero de lineas': 100, 'Numero de palabras': 450, 'Numero de caracteres': 2340}
  ```

* Imprimir líneas 10 a 20 junto con la información:

  ```bash
  python info_txt.py documento.txt 10:20
  # Salida:
  # {'Numero de lineas': 100, 'Numero de palabras': 450, 'Numero de caracteres': 2340}
  # Líneas solicitadas:
  # 10: Texto de ejemplo...
  # ...
  ```

## Opciones o configuración

* **`file_path`**: (requerido) Ruta al archivo de texto.
* **`line_range`**: (opcional) Rango de líneas a imprimir. Si no se especifica, solo se muestra la información básica.

---

*Generado automáticamente.*
