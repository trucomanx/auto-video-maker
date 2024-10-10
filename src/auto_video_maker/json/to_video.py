#!/usr/bin/python3


import auto_video_maker as avm

import json
from moviepy.editor import ImageClip, VideoFileClip, AudioClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips
import os

def concat_videos_memory(video_paths, output_path):
    """
    Concatenates multiple video files into a single video file while managing memory efficiently.

    Parameters:
    video_paths (list of str): A list of file paths to the video files that need to be concatenated.
    output_path (str): The file path where the final concatenated video will be saved.

    Note:
    - When the input videos have different resolutions (width and height), 
      the `concatenate_videoclips` function will raise an exception. 
      To avoid this issue, it is advisable to resize all videos to a 
      common resolution before concatenation. This can be accomplished 
      by using the `resize` method from the `VideoFileClip` class to ensure 
      that all clips are of the same size.
    - This method spend a lot of memory but is speed.

    Example:
    video_paths = ['video1.mp4', 'video2.mp4', 'video3.mp4']
    output_path = 'final_video.mp4'
    concat_videos_memory(video_paths, output_path)
    """
    # Agora, carregamos os vídeos temporários e concatenamos
    final_clips = [VideoFileClip(video) for video in video_paths]
    final_video = concatenate_videoclips(final_clips)

    # Exporta o vídeo final
    final_video.write_videofile(output_path)
    
    
def concat_videos_recursively(video_paths, output_path, idx=0):
    """
    Recursively concatenates a list of video files into a single video file.

    This function divides the list of video paths into two halves and concatenates 
    them recursively until only one video remains. It can handle video files of 
    different sizes by adjusting their dimensions to match the smallest video 
    in each concatenation step. 

    Parameters:
    - video_paths (list): A list of strings representing the paths to the video files to be concatenated.
    - output_path (str): The path where the final concatenated video will be saved.
    - idx (int): An index used for naming temporary output files during recursion. 
                 It defaults to 0 for the initial call.

    Returns:
    - str: The path to the final concatenated video file.

    Notes:
    - The function creates temporary video files during the recursive process, which are deleted 
      once they are no longer needed.
    - Ensure that the necessary video codecs and formats are available for writing the final output.
    
    Handling Different Video Sizes:
    - When videos of different sizes are concatenated, it is important to ensure that they match in dimensions.
    - This implementation can be modified to resize the videos to a common size before concatenation. 
      For example, using `resize()` from MoviePy can help in making all videos the same size. 
    - This ensures that the final output video has a uniform appearance without unexpected artifacts 
      due to differing video dimensions.
    """
    # Base da recursão: Se houver apenas um vídeo na lista, retorne-o
    if len(video_paths) == 1:
        return video_paths[0]
    
    # Divide a lista de vídeos em duas partes
    mid = len(video_paths) // 2
    left_videos = video_paths[:mid]
    right_videos = video_paths[mid:]
    
    # Concatena recursivamente a lista da esquerda e da direita
    left_output = concat_videos_recursively(left_videos, f'temp_left_{idx}.mp4', idx * 2 + 1)
    right_output = concat_videos_recursively(right_videos, f'temp_right_{idx}.mp4', idx * 2 + 2)
    
    # Carrega os vídeos resultantes da esquerda e direita
    left_clip = VideoFileClip(left_output)
    right_clip = VideoFileClip(right_output)
    
    # Concatena os dois vídeos
    final_clip = concatenate_videoclips([left_clip, right_clip])
    
    # Salva o vídeo concatenado 
    final_clip.write_videofile(output_path, codec="libx264")
    
    # Fecha os clipes para liberar memória
    left_clip.close()
    right_clip.close()
    
    # Remove os vídeos temporários intermediários
    if os.path.exists(left_output):
        os.remove(left_output)
    if os.path.exists(right_output):
        os.remove(right_output)
    
    return output_path
    
def create_silence(duration, fps=44100):
    """
    Cria um clipe de áudio de silêncio com uma duração específica.

    :param duration: Duração do clipe de silêncio em segundos.
    :param fps: Frequência de amostragem do áudio (padrão: 44100 Hz).
    :return: Um clipe de áudio contendo silêncio.
    """
    return AudioClip(lambda t: [0], duration=duration, fps=fps)

def to_video(   file_path, 
                basedir,
                config_path,
                temp_folder = "temp_videos",
                output_path="video_final.mp4",
                codec="libx264", 
                audio_codec="aac",
                fps=25,
                transicion_duration = 1):
    # Carregar o arquivo JSON
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Carregar o arquivo JSON
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    # Pasta para salvar os vídeos temporários
    os.makedirs(temp_folder, exist_ok=True)

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
                    
        temp_video_path = os.path.join(temp_folder, f"video_{idx}.mp4")
        
        # Cria um ImageClip a partir da imagem
        video_clip = None;
        img_rel_path = visual.get('source', '')
        
        if img_rel_path!="" and visual.get("enable"):
            img_path = os.path.join(basedir,img_rel_path);
            video_clip = ImageClip(img_path).set_duration(config["time_minimum"])  # duração do vídeo
        else:
            # Cria um clipe de cor (preto) com a mesma duração do áudio
            video_clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=config["time_minimum"])

        # Carrega o áudio
        temp_audio_path="";
        raw_text = textual.get('source', '').strip();
        if raw_text!="" and textual.get("enable"):
            temp_audio_path=os.path.join(temp_folder,f"audio_{idx}.mp3");
            avm.text.to_audio(raw_text, temp_audio_path, lang=None);
            audio_clip = AudioFileClip(temp_audio_path)
            
            if (audio_clip.duration+transicion_duration)<video_clip.duration :
                t=video_clip.duration-audio_clip.duration-transicion_duration
                audio_clip = concatenate_audioclips([   create_silence(transicion_duration, fps=audio_clip.fps), 
                                                        audio_clip,
                                                        create_silence(t, fps=audio_clip.fps)])
            else:
                audio_clip = concatenate_audioclips([create_silence(transicion_duration, fps=audio_clip.fps), audio_clip])
    

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
        
        #if os.path.exists(temp_audio_path):
        #    os.remove(temp_audio_path)
        
        # Adiciona o caminho do vídeo temporário à lista
        temp_videos.append(temp_video_path)
    
    #concat_videos_recursively(temp_videos, output_path)
    #concat_videos_memory(temp_videos, output_path)
    avm.video.concatenate_in_batches(   temp_videos, 
                                        output_path,
                                        batch_size=5,
                                        transicion_duration = transicion_duration,
                                        transicion_type="slide-left",#"crossfade",#
                                        codec=codec, 
                                        audio_codec=audio_codec,
                                        fps=fps)

    
