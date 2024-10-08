#!/usr/bin/python3

import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_image(pdf_path, output_dir, image_name_format):
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
        pix = page.get_pixmap(dpi=300, annots=False)
        
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

# Exemplo de uso
list_path_of_images = pdf_to_image("main.pdf", "output/images", "image%d.png")
print(list_path_of_images)

