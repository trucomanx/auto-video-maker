#!/usr/bin/python3

import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_image(pdf_path, output_dir, image_name_format, dpi=300):
    """
    Converts each page of a PDF file into an image and saves them in a specified output directory.

    Parameters:
    -----------
    pdf_path : str
        Path to the PDF file to be converted.
    
    output_dir : str
        Directory where the generated images will be saved.
    
    image_name_format : str
        A format string for naming the output images, which should contain a placeholder for the page number.
        Example: 'page_%d.png'
    
    dpi : int, optional (default=300)
        The resolution (dots per inch) for rendering the PDF pages as images.

    Returns:
    --------
    image_paths : list of str
        A list of file paths where the images generated from the PDF pages are saved.

    Example Usage:
    --------------
    pdf_to_image('example.pdf', 'output_images', 'page_%d.png')

    Notes:
    ------
    - Uses PyMuPDF (`fitz`) to load and render each PDF page.
    - Each page is rendered at the specified DPI resolution and saved as a PNG image.
    - The function creates the output directory if it does not already exist.
    """
    # Abrir o PDF
    pdf_document = fitz.open(pdf_path)

    # Garantir que o diretório de saída exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lista para armazenar os paths das imagens geradas
    image_paths = []

    # Iterar sobre todas as páginas do PDF
    for page_num in range(pdf_document.page_count):
        # Carregar a página
        page = pdf_document.load_page(page_num)

        # Renderizar a página como uma imagem em alta resolução (300 dpi), sem anotações
        pix = page.get_pixmap(dpi=dpi, annots=False)
        
        # Definir o nome da imagem de acordo com o formato especificado
        image_path = os.path.join(output_dir, image_name_format % page_num)

        # Salvar a imagem no formato PNG
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save(image_path)

        # Adicionar o caminho da imagem à lista
        image_paths.append(image_path)

    # Fechar o documento PDF
    pdf_document.close()

    return image_paths

################################################################################

if __name__ == '__main__':
    # Exemplo de uso
    list_path_of_images = pdf_to_image("main.pdf", "output/images", "image%d.png")
    print(list_path_of_images)

