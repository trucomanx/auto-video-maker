#!/usr/bin/python3

from moviepy.editor import transfx

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
        clips_with_transitions.append( clips[i].fx( transfx.slide_in, duration, side) )
    
    return clips_with_transitions
