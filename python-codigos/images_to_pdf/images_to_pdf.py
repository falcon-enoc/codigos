import os
import argparse
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import blue, black, darkblue  # Añadido más colores para mejor contraste


def images_to_pdf(folder_path, output_pdf):
    # Gather image files
    supported_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    files = sorted(
        f for f in os.listdir(folder_path)
        if f.lower().endswith(supported_exts)
    )

    if not files:
        print("No se encontraron imágenes en la carpeta especificada.")
        return

    # Create PDF canvas
    c = canvas.Canvas(output_pdf)

    for filename in files:
        file_path = os.path.join(folder_path, filename)

        # Title is filename without extension
        title = os.path.splitext(filename)[0]

        # Open image to get size
        with Image.open(file_path) as img:
            width_px, height_px = img.size

        # Calculate image dimensions at 80% of original size
        img_width = width_px * 0.8
        img_height = height_px * 0.8
        
        # Calculate margins to center the image
        horizontal_margin = (width_px - img_width) / 2
        
        # Add more space for the title
        title_space = 1.5 * inch  # 1 inch for title space
        
        # Set page dimensions
        page_width = width_px
        page_height = img_height + title_space

        # Set the page size
        c.setPageSize((page_width, page_height))

        # Draw title with better visibility
        c.setFont("Helvetica-Bold", 60)  # Increased font size from 14 to 24
        c.setFillColor(darkblue)  # Changed from red to darkblue for better contrast
        text_x = page_width / 2  # Center horizontally
        text_y = page_height - (title_space / 2)  # Position in the middle of title space
        
        # Draw centered text
        c.drawCentredString(text_x, text_y, title)

        # Draw image with margin at the top for the title and scaled to 80%
        img_x = horizontal_margin
        img_y = 0  # Bottom of the page
        c.drawImage(file_path, img_x, img_y, width=img_width, height=img_height)

        # Finish the page
        c.showPage()

    # Save the PDF
    c.save()
    print(f"PDF generado exitosamente: {output_pdf}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convierte todas las imágenes en una carpeta en un PDF, una por página, con el título tomado del nombre de archivo.'
    )
    parser.add_argument(
        'folder',
        help='Ruta de la carpeta que contiene las imágenes'
    )
    parser.add_argument(
        '-o', '--output',
        help='Ruta del archivo PDF de salida. Si no se especifica, se guardará en el directorio actual.',
        default=None
    )
    args = parser.parse_args()
    
    # Si no se especifica la ruta de salida, usar el directorio actual
    if args.output is None:
        # Obtener el nombre de la carpeta de imágenes para usarlo como nombre del PDF
        folder_name = os.path.basename(os.path.normpath(args.folder))
        output_pdf = os.path.join(os.getcwd(), f"{folder_name}.pdf")
    else:
        output_pdf = args.output
    
    images_to_pdf(args.folder, output_pdf)
