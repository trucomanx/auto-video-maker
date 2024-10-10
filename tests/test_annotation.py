#!/usr/bin/python

import sys
sys.path.append('../src')


import json
import auto_video_maker as avm

pdf_file = "/home/fernando/Proyectos/AULAS Y EXPOS/CURSOS/NeuralNetwork/conv2d/main.pdf"
all_annotations = avm.pdf.annotations(pdf_file)


for page, annotations in enumerate(all_annotations):
    print("page:",page)
    for idx, annotation in enumerate(annotations):
        print("idx:",idx)
        print(json.dumps(annotation, indent=4))
