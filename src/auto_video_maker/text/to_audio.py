#!/usr/bin/python3

from gtts import gTTS
from langdetect import detect

def detect_language(text):
    """
    Detecta o idioma do texto usando a biblioteca langdetect.

    :param text: Texto para detecção de idioma.
    :return: Código do idioma detectado (ex: 'en' para inglês, 'pt' para português).
    """
    try:
        language = detect(text)
        return language
    except Exception as e:
        print(f"Ocorreu um erro ao detectar o idioma: {e}")
        print("Set en by default")
        return "en"

def to_audio_with_gtts(text, filename='output.mp3', lang=None):
    """
    Converte texto em arquivo de áudio usando gTTS com autodetecção de idioma, se necessário.

    :param text: Texto a ser convertido.
    :param filename: Nome do arquivo de áudio de saída (padrão: 'output.mp3').
    :param lang: Idioma do texto (padrão: None para autodetecção).
    """
    try:
        if lang is None:
            lang = detect_language(text)
        
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        print(f"Áudio salvo como {filename}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def to_audio(text, filename='output.mp3', lang=None, method="gtts"):
    if method=="gtts":
        to_audio_with_gtts(text, filename, lang)
    else:
        exit();
