# Este script proporciona información básica sobre un archivo de texto, como el número de líneas,
# el número de palabras y el número de caracteres del archivo. Además, permite al usuario especificar
# opcionalmente un rango de líneas para imprimir del archivo. El rango puede ser especificado en varios
# formatos como "inicio:fin", ":fin" o "inicio:", donde se imprimen las líneas comprendidas en ese rango.
# Si no se especifica ningún rango, solo se imprime la información básica del archivo.

# Funcionalidades principales:
# - Leer un archivo de texto y calcular el número de líneas, palabras y caracteres.
# - Imprimir un rango de líneas especificado por el usuario, en caso de que se indique.
# - Manejar errores como archivos no encontrados y rango de líneas inválidos.

import argparse

def informacion_basica_txt(file_path, line_range=None):
    """
    Esta función recibe la ruta de un archivo de texto y opcionalmente un rango de líneas a imprimir.
    También devuelve información básica sobre el archivo: número de líneas, número de palabras y número de caracteres.
    """
    num_lineas = 0
    num_palabras = 0
    num_caracteres = 0
    lineas_a_imprimir = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lineas = file.readlines()
            num_lineas = len(lineas)
            for linea in lineas:
                palabras = linea.split()
                num_palabras += len(palabras)
                num_caracteres += len(linea)

            if line_range:
                start, end = parse_line_range(line_range, num_lineas)
                lineas_a_imprimir = lineas[start:end]

        info = {
            'Numero de lineas': num_lineas,
            'Numero de palabras': num_palabras,
            'Numero de caracteres': num_caracteres
        }
        
        return info, lineas_a_imprimir
    except FileNotFoundError:
        return "El archivo no se encontró.", []
    except Exception as e:
        return f"Ocurrió un error: {e}", []

def parse_line_range(line_range, num_lineas):
    """
    Esta función convierte el rango de líneas en índices de inicio y fin.
    """
    if ':' in line_range:
        start, end = line_range.split(':')
        start = int(start) - 1 if start else 0
        end = int(end) if end else num_lineas
    else:
        start = int(line_range) - 1
        end = start + 1

    return max(start, 0), min(end, num_lineas)

def main():
    parser = argparse.ArgumentParser(description='Obtener información básica de un archivo de texto y opcionalmente imprimir un rango de líneas.')
    parser.add_argument('file_path', type=str, help='Ruta del archivo de texto')
    parser.add_argument('line_range', type=str, nargs='?', help='Rango de líneas a imprimir (por ejemplo, 10, 10:20, :10, 10:)', default=None)
    args = parser.parse_args()
    
    info, lineas_a_imprimir = informacion_basica_txt(args.file_path, args.line_range)
    
    print(info)
    if lineas_a_imprimir:
        print("\nLíneas solicitadas:\n")
        for linea in lineas_a_imprimir:
            print(linea, end='')

if __name__ == '__main__':
    main()
