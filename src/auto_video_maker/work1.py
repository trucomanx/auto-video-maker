#!/usr/bin/python3

# pip install pymupdf

import fitz  # PyMuPDF

# Função para extrair todas as anotações (comentários) de todas as páginas de um PDF
def extract_all_annotations(pdf_path):
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

# Exemplo de uso
pdf_file = "main.pdf"
all_comments = extract_all_annotations(pdf_file)

# Exibindo os resultados
for page_num, comments in enumerate(all_comments):
    print(f"Anotações na página {page_num + 1}:")
    if comments:
        for comment in comments:
            print(f"  Tipo: {comment['type']}, Conteúdo: {comment['content']}, Localização: {comment['rect']}")
    else:
        print("  Sem anotações.")


