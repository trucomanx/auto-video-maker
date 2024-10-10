#!/usr/bin/python3

from moviepy.editor import AudioClip

def silence(duration, fps=44100):
    """
    Cria um clipe de áudio de silêncio com uma duração específica.

    :param duration: Duração do clipe de silêncio em segundos.
    :param fps: Frequência de amostragem do áudio (padrão: 44100 Hz).
    :return: Um clipe de áudio contendo silêncio.
    """
    return AudioClip(lambda t: [0], duration=duration, fps=fps)
