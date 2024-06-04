import pandas as pd
import sys
import os

def excel_to_txt(excel_file):
    # Obtener el nombre base del archivo (sin extensión)
    base_name = os.path.splitext(excel_file)[0]
    # Crear el nombre del archivo de texto de salida
    txt_file = f"{base_name}.txt"
    
    # Leer el archivo Excel
    df = pd.read_excel(excel_file)
    
    # Abrir el archivo de texto para escribir
    with open(txt_file, 'w', encoding='utf-8') as f:
        # Iterar sobre cada fila del DataFrame
        for index, row in df.iterrows():
            # Convertir la fila en una cadena de texto
            row_str = '\t'.join(row.astype(str).values)
            # Escribir la cadena en el archivo de texto
            f.write(row_str + '\n')

    print(f"Archivo de texto '{txt_file}' generado exitosamente.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <archivo_excel>")
        sys.exit(1)

    excel_file = sys.argv[1]  # Primer argumento: archivo Excel

    excel_to_txt(excel_file)
