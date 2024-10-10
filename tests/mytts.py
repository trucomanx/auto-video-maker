#!/usr/bin/python

# pip install TTS ## Muito pesado ne sei quanto


from TTS.api import TTS

# Baixando e carregando um modelo pré-treinado (por exemplo, para PT-BR)
tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False)

# Texto a ser convertido em fala
text = "Olá, como você está?"

# Convertendo o texto para fala e salvando em um arquivo de áudio
tts.tts_to_file(text=text, file_path="output_coqui_tts.wav")

print("Áudio gerado: output_coqui_tts.wav")

