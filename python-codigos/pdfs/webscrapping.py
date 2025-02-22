import requests
from bs4 import BeautifulSoup
import os

# URL de la página que contiene los PDF
url = 'https://www.ccu.cl/publicaciones-ccu/'

# Realizar la solicitud GET para obtener el contenido de la página
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Crear una carpeta para almacenar los PDFs descargados
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')

    # Buscar todos los enlaces que contienen archivos PDF
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf'):
            pdf_url = link['href']
            
            # Asegurarse de que el enlace es absoluto
            if not pdf_url.startswith('http'):
                pdf_url = f'https://www.ccu.cl{pdf_url}'
            
            # Descargar el PDF
            pdf_response = requests.get(pdf_url)
            pdf_name = pdf_url.split('/')[-1]

            # Guardar el PDF en la carpeta 'pdfs'
            with open(f'pdfs/{pdf_name}', 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f'Descargado: {pdf_name}')
else:
    print(f'Error al acceder a la página: {response.status_code}')
