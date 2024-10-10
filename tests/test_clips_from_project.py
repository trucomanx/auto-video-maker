#!/usr/bin/python3

# pip install moviepy
import sys
sys.path.append('../src')


import auto_video_maker as avm



    
pdf_file = "/home/fernando/Proyectos/AULAS Y EXPOS/CURSOS/NeuralNetwork/conv2d/main.pdf"


avm.pdf.to_project(pdf_file, "output", "image%d.png", dpi=300)


temp_videos = avm.video.clips_from_project( "output/data.json",
                                            "output",
                                            "output/config.json",
                                            output_dir = "temp_videos",
                                            name_format = "video_%d.mp4",
                                            codec="libx264", 
                                            audio_codec="aac",
                                            fps=25,
                                            offset_audio_init=1.1,
                                            offset_audio_end=1.1)



