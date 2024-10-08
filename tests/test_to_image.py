#!/usr/bin/python

import sys
sys.path.append('../src')


import auto_video_maker as avm

pdf_file = "/home/fernando/Proyectos/AULAS Y EXPOS/CURSOS/NeuralNetwork/conv2d/main.pdf"


list_path_of_images = avm.pdf.to_images(pdf_file, "output", "image%d.png")
print(list_path_of_images)
