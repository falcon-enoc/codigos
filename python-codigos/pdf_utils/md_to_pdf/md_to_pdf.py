import argparse
import os
from markdown_pdf import MarkdownPdf, Section

def main():
    parser = argparse.ArgumentParser(description='Convierte un archivo Markdown a PDF.')
    parser.add_argument('markdown_file', help='La ruta al archivo Markdown a convertir.')
    parser.add_argument('-o', '--output', help='El directorio de salida para el archivo PDF. Por defecto, es el directorio del script.')
    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print(f'Error: El archivo {args.markdown_file} no existe.')
        return

    output_dir = args.output if args.output else os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(args.markdown_file))[0] + '.pdf')

    try:
        with open(args.markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        pdf = MarkdownPdf()
        pdf.add_section(Section(markdown_content))
        pdf.save(pdf_file_path)
        print(f'¡El archivo {args.markdown_file} se ha convertido a {pdf_file_path} exitosamente!')
    except Exception as e:
        print(f'Error al convertir el archivo: {e}')

if __name__ == '__main__':
    main()
