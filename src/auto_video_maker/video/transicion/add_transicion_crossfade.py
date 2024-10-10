#!/usr/bin/python3

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
