#!/usr/bin/python3

# pip install pymupdf

import fitz  # PyMuPDF

# Função para extrair todas as anotações (comentários) de todas as páginas de um PDF
def pdf_annotations(pdf_path):
    """
    Extracts annotations from a PDF file and returns a list of dictionaries containing
    information about the annotations on each page.

    Parameters:
    -----------
    pdf_path : str
        Path to the PDF file to be processed.

    Returns:
    --------
    all_annotations : list of lists of dict
        A list where each item corresponds to a page in the PDF, containing a list of dictionaries 
        with details about the annotations on that page. Each annotation dictionary includes:
            - 'type': The type of annotation (e.g., text, highlight).
            - 'content': The content of the annotation (if available).
            - 'rect': The coordinates of the annotation's position on the page (rectangle).

    Example Return:
    -------------------
    [
        [   # Page 1
            {'type': 'Text', 'content': 'Comment', 'rect': (x0, y0, x1, y1)},
            {'type': 'Highlight', 'content': 'Highlighted text', 'rect': (x0, y0, x1, y1)}
        ],
        [   # Page 2
            {'type': 'Text', 'content': 'Another comment', 'rect': (x0, y0, x1, y1)}
        ],
        ...
    ]

    Notes:
    ------
    - Uses the PyMuPDF library (imported as `fitz`) to open the PDF file and access annotations.
    - Automatically closes the PDF document after processing.

    """
    # Abre o arquivo PDF
    pdf_document = fitz.open(pdf_path)

    # Lista para armazenar os comentários de cada página
    all_annotations = []

    # Percorre todas as páginas do PDF
    for page_num in range(pdf_document.page_count):
        # Carrega a página
        page = pdf_document.load_page(page_num)

        # Lista para armazenar as anotações desta página
        page_annotations = []

        # Itera sobre as anotações da página
        for annot in page.annots():
            annot_info = {
                'type': annot.type[1],  # Tipo de anotação (e.g., texto, highlight)
                'content': annot.info.get("content", ""),  # Conteúdo da anotação
                'rect': annot.rect  # Posição da anotação na página
            }
            page_annotations.append(annot_info)

        # Adiciona a lista de anotações da página à lista principal
        all_annotations.append(page_annotations)

    # Fecha o documento PDF
    pdf_document.close()

    return all_annotations

################################################################################

if __name__ == '__main__':
    # Exemplo de uso
    pdf_file = "main.pdf"
    all_comments = pdf_annotations(pdf_file)

    # Exibindo os resultados
    for page_num, comments in enumerate(all_comments):
        print(f"Anotações na página {page_num + 1}:")
        if comments:
            for comment in comments:
                print(f"  Tipo: {comment['type']}, Conteúdo: {comment['content']}, Localização: {comment['rect']}")
        else:
            print("  Sem anotações.")


