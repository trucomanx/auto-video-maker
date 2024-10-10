#!/usr/bin/python3


import auto_video_maker as avm

import json
from moviepy.editor import ImageClip 
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import auto_video_maker as avm

    

    


def clips_from_project( file_path, 
                        base_dir,
                        config_path,
                        output_dir = "temp_videos",
                        name_format = "video_%d.mp4",
                        codec="libx264", 
                        audio_codec="aac",
                        fps=25,
                        offset_audio_init = 1,
                        offset_audio_end = 1):
    # Carregar o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Carregar o arquivo JSON
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    # Pasta para salvar os vídeos temporários
    os.makedirs(output_dir, exist_ok=True)

    # Lista para armazenar os caminhos dos vídeos temporários
    temp_videos = []
    
    # Processar o JSON conforme necessário
    width = data.get("width")
    height = data.get("height")
    clips = data.get("clips", [])
    
    print(f"Largura: {width}, Altura: {height}")
    for idx, clip in enumerate(clips):
        textual = clip.get("textual", {})
        visual = clip.get("visual", {})
        
        print("")
        print("idx",idx,"until",len(clips)-1)
                    
        temp_video_path = os.path.join(output_dir, name_format % idx)
        
        # Cria um ImageClip a partir da imagem
        video_clip = None;
        img_rel_path = visual.get('source', '')
        
        if img_rel_path!="" and visual.get("enable"):
            img_path = os.path.join(base_dir,img_rel_path);
            video_clip = ImageClip(img_path).set_duration(config["time_minimum"])  # duração do vídeo
        else:
            # Cria um clipe de cor (preto) com a mesma duração do áudio
            video_clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=config["time_minimum"])

        # Carrega o áudio
        temp_audio_path="";
        raw_text = textual.get('source', '').strip();
        if raw_text!="" and textual.get("enable"):
            temp_audio_path=os.path.join(output_dir,f"audio_{idx}.mp3");
            avm.text.to_audio(raw_text, temp_audio_path, lang=None);
            audio_clip = AudioFileClip(temp_audio_path)
            
            if (audio_clip.duration+offset_audio_init+offset_audio_end)<video_clip.duration :
                t=video_clip.duration-audio_clip.duration-offset_audio_init-offset_audio_end
                audio_clip = concatenate_audioclips([   avm.audio.silence(offset_audio_init, fps=audio_clip.fps), 
                                                        audio_clip,
                                                        avm.audio.silence(offset_audio_end, fps=audio_clip.fps),
                                                        avm.audio.silence(t, fps=audio_clip.fps)])
            else:
                audio_clip = concatenate_audioclips([   avm.audio.silence(offset_audio_init, fps=audio_clip.fps), 
                                                        audio_clip,
                                                        avm.audio.silence(offset_audio_end, fps=audio_clip.fps)])
    

            duration = max(audio_clip.duration,video_clip.duration);
            
            # Define o áudio para o ImageClip
            audio_clip = audio_clip.set_duration(duration)
            video_clip = video_clip.set_audio(audio_clip)
            
            # Ajusta a duração do vídeo de acordo com o áudio
            video_clip = video_clip.set_duration(duration)
            
        else:
            print("")
            print(f"{temp_video_path} without audio!\n")
    
        # Salva o vídeo temporário
        video_clip.write_videofile(temp_video_path, codec=codec, audio_codec=audio_codec,fps=fps)
        
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        # Adiciona o caminho do vídeo temporário à lista
        temp_videos.append(temp_video_path)
    
    
    return temp_videos


    
