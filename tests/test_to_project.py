#!/usr/bin/python3

import sys
sys.path.append('../src')


import auto_video_maker as avm

pdf_file = "/home/fernando/Proyectos/AULAS Y EXPOS/CURSOS/NeuralNetwork/conv2d/main.pdf"


avm.pdf.to_project(pdf_file, "output", "image%d.png", dpi=300, shape=(800,600))
