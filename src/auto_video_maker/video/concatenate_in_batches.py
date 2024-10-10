#!/usr/bin/python3

import os
import tempfile
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import transfx
from collections import Counter

def most_frequent_size(clips):
    """
    Finds the most frequent width and height among the given video clips.

    Parameters:
    - clips (list): A list of VideoFileClip objects.

    Returns:
    - tuple: A tuple containing the most frequent width and height (width, height).
    """
    sizes = [(clip.w, clip.h) for clip in clips]
    
    # Conta as ocorrências de cada par de dimensões (largura, altura)
    size_counter = Counter(sizes)
    
    # Obtém o tamanho (largura, altura) mais comum
    most_frequent = size_counter.most_common(1)[0][0]
    
    return most_frequent

def resize_clips_to_most_frequent(clips):
    """
    Resizes the given video clips to the most frequent dimensions.

    Parameters:
    - clips (list): A list of VideoFileClip objects to be resized.

    Returns:
    - list: A list of resized VideoFileClip objects.
    """
    # Encontra o tamanho mais frequente (largura e altura)
    most_frequent_width, most_frequent_height = most_frequent_size(clips)
    
    # Redimensiona os clipes para o tamanho mais frequente
    resized_clips = [clip.resize(newsize=(most_frequent_width, most_frequent_height)) for clip in clips]
    return resized_clips

def add_transicion_crossfade(clips, duration=1):
    """
    Adds crossfade transitions between the video clips.

    Parameters:
    - clips (list): A list of VideoFileClip objects.
    - duration (int): The duration of the crossfade in seconds.

    Returns:
    - list: A list of VideoFileClip objects with crossfades applied.
    """
    # Aplica o efeito crossfade entre os clipes
    clips_with_transitions = [clips[0]]  # Começa com o primeiro clipe sem transição
    for i in range(1, len(clips)):
        # Aplica a transição de crossfade entre o clipe anterior e o próximo
        clips_with_transitions.append(clips[i].crossfadein(duration))
    
    return clips_with_transitions

def add_transicion_slide(clips, duration=1, side='left'):
    """
    Adds slide transitions between the video clips.

    Parameters:
    - clips (list): A list of VideoFileClip objects.
    - duration (int): The duration of the crossfade in seconds.

    Returns:
    - list: A list of VideoFileClip objects with slide applied.
    """
    # Aplica o efeito crossfade entre os clipes
    clips_with_transitions = [clips[0]]  # Começa com o primeiro clipe sem transição
    for i in range(1, len(clips)):
        # Aplica a transição de crossfade entre o clipe anterior e o próximo
        clips_with_transitions.append( clips[i].fx( transfx.slide_in, 1, side) )
    
    return clips_with_transitions

def concatenate_in_batches( video_paths, 
                            output_path, 
                            batch_size=5,
                            transicion_duration = 1,
                            transicion_type="crossfade",
                            codec="libx264", 
                            audio_codec="aac",
                            fps=25):
    """
    Concatenates a list of video files in batches to manage memory efficiently.

    Parameters:
    - video_paths (list): A list of strings representing the paths to the video files to be concatenated.
    - output_path (str): The path where the final concatenated video will be saved.
    - batch_size (int): The number of videos to process in each batch.
    
    Returns:
    - str: The path to the final concatenated video file.
    """
    
    # Lista para armazenar o caminho dos vídeos temporários concatenados
    temp_outputs = []

    # Processa os vídeos em lotes
    for i in range(0, len(video_paths), batch_size):
        batch = video_paths[i:i + batch_size]
        
        # Carrega os vídeos do lote
        clips = [VideoFileClip(video) for video in batch]
        
        # Redimensiona os clipes para as dimensões mínimas
        clips = resize_clips_to_most_frequent(clips)
        
        # Adiciona transições (crossfades) entre os clipes
        if transicion_type=="crossfade":
            clips = add_transicion_crossfade(clips, duration=transicion_duration)
        elif transicion_type=="slide-left":
            clips = add_transicion_slide(clips, duration=transicion_duration, side='left')

        # Concatena os vídeos do lote usando o método "compose" para evitar degradação
        concatenated_clip = concatenate_videoclips(clips, method="compose",padding=transicion_duration)

        # Cria um arquivo temporário para salvar o vídeo concatenado do lote
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_output_path = temp_file.name
            
        # Salva o vídeo concatenado do lote
        concatenated_clip.write_videofile(temp_output_path, codec=codec, audio_codec=audio_codec,fps=fps)
        
        # Fecha os clipes para liberar memória
        for clip in clips:
            clip.close()
        
        # Adiciona o caminho do vídeo temporário à lista
        temp_outputs.append(temp_output_path)
        
    # Concatena todos os vídeos temporários gerados usando o método "compose"
    final_clips = [VideoFileClip(temp_output) for temp_output in temp_outputs]

    if transicion_type=="crossfade":
        final_clips = add_transicion_crossfade(final_clips, duration=transicion_duration)
    elif transicion_type=="slide-left":
        final_clips = add_transicion_slide(final_clips, duration=transicion_duration, side='left')
        
    final_clip = concatenate_videoclips(final_clips, method="compose",padding=transicion_duration)
    
    # Salva o vídeo final
    final_clip.write_videofile(output_path, codec=codec, audio_codec=audio_codec,fps=fps)
    
    # Fecha os clipes finais
    for clip in final_clips:
        clip.close()

    # Remove os arquivos temporários
    for temp_output in temp_outputs:
        if os.path.exists(temp_output):
            os.remove(temp_output)

    return output_path
'''
# Exemplo de uso
video_files = ['video1.mp4', 'video2.mp4', 'video3.mp4', ...]  # Adicione seus caminhos de vídeo
output_file = 'final_output.mp4'
concat_videos_in_batches(video_files, output_file)
'''
