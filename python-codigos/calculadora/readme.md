# Calculadora Python

## Descripción

`calculadora` es un sencillo módulo en Python que permite realizar operaciones aritméticas básicas: suma, resta, multiplicación y división. Está pensado para integrarse fácilmente en otros proyectos o para usarse como ejemplo de funciones en Python.

## Instalación

1. Asegúrate de tener Python 3 instalado en tu sistema.

2. (Opcional) Crea un entorno virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. No hay dependencias externas, así que no es necesario instalar paquetes adicionales.

## Uso

Importa la función `calculadora` en tu script o ejecuta el módulo directamente desde la línea de comandos.

### Como módulo

```python
from calculadora import calculadora

# Ejemplos:
print(calculadora(5, 3, "+"))  # 8
print(calculadora(10, 4, "-"))  # 6
print(calculadora(6, 7, "*"))  # 42
print(calculadora(8, 2, "/"))  # 4.0
```

### Directamente desde la línea de comandos

```bash
python calculadora.py
```

Por defecto, el archivo imprimirá el resultado de `calculadora(2, 0, "/")`, que es `error`.

## Opciones o configuración

La función `calculadora` acepta tres parámetros:

* `n1` (numérico): Primer operando.
* `n2` (numérico): Segundo operando.
* `op` (str): Operador, uno de:

  * `"+"`: Suma.
  * `"-"`: Resta.
  * `"*"`: Multiplicación (si alguno de los operandos es 0, devuelve 0).
  * `"/"`: División (si `n2` es 0, devuelve la cadena "error").

No hay variables de entorno ni banderas adicionales.

