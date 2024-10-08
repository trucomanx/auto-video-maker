#!/usr/bin/python

import sys
sys.path.append('../src')



import auto_video_maker as avm

pdf_file = "/home/fernando/Proyectos/AULAS Y EXPOS/CURSOS/NeuralNetwork/conv2d/main.pdf"
all_comments = avm.pdf.annotations(pdf_file)

# Exibindo os resultados
for page_num, comments in enumerate(all_comments):
    print(f"Anotações na página {page_num + 1}:")
    if comments:
        for comment in comments:
            print(f"  Tipo: {comment['type']}, Conteúdo: {comment['content']}, Localização: {comment['rect']}")
    else:
        print("  Sem anotações.")

