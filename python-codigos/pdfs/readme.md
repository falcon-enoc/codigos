
# Descargador de PDFs (WebScrapping.py)

## Descripción

Este proyecto ofrece un script en Python que descarga automáticamente todos los archivos PDF listados en una página web (en este caso, [https://www.ccu.cl/publicaciones-ccu/](https://www.ccu.cl/publicaciones-ccu/)). Utiliza `requests` para realizar peticiones HTTP y `BeautifulSoup` para parsear el HTML y extraer los enlaces de los PDF.

## Instalación

1. Asegúrate de tener Python 3.6 o superior.
2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:

   ```bash
   pip install requests beautifulsoup4
   ```

## Uso

1. **Configurar la URL** (si deseas apuntar a otra página):

   * Edita la variable `url` en el script.

2. **Ejecutar el script**:

   ```bash
   python descargar_pdfs.py
   ```

   * El script crea una carpeta `pdfs/` en el directorio actual (si no existe).
   * Descarga cada PDF encontrado y lo guarda en `pdfs/`.

3. **Ejemplo de salida**:

   ```console
   Descargado: informe-enero-2025.pdf
   Descargado: resultados-financieros.pdf
   ```

## Opciones o configuración

* **`url`**: URL de la página que contiene enlaces a PDFs. Por defecto:

  ```python
  url = 'https://www.ccu.cl/publicaciones-ccu/'
  ```
* **Carpeta de salida**: El script guarda los PDF en la carpeta `pdfs/`.

  * Para cambiarla, modifica el nombre en el bloque de creación:

    ```python
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')
    ```

---

*Generado automáticamente.*
