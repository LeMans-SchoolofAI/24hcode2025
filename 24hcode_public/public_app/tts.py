import torch, os
from TTS.api import TTS

#get current path
MEDIA_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))+ "/media/"  # just "/media" si docker
print(MEDIA_PATH)

# auto downloaded models are in /home/<user>/.local/share/tts/

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
# print(TTS().list_models())

# Init TTS
## tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
## wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
# Text to speech to a file
## tts.tts_to_file(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")

# Init TTS with the target model name
# tts = TTS(model_name="tts_models/fr/mai/tacotron2-DDC", progress_bar=True).to(device)

# # Run TTS
# tts.tts_to_file(text="Bonjour, bienvenue aux vingt-quatre heures du code, comment puis-je vous aider ?", file_path=MEDIA_PATH+"output_24h.wav")

# tts = TTS(model_name="tts_models/fr/css10/vits", progress_bar=True).to(device)

# # Run TTS
# tts.tts_to_file(text="Bonjour, bienvenue aux vingt-quatre heures du code, comment puis-je vous aider ?", file_path=MEDIA_PATH+"output_242h.wav")

# # Init TTS with the target model name
# tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True).to(device)

# # Run TTS
# tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=MEDIA_PATH+"output_DE.wav")

# Example voice cloning with YourTTS in English, French and Portuguese
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True).to(device)
# tts.tts_to_file("This is voice cloning.", speaker_wav=MEDIA_PATH+"pierre.wav", language="en", file_path=MEDIA_PATH+"output_EN.wav")
tts.tts_to_file("Bonjour, bienvenue aux vingt-quatre heures du code, comment puis-je vous aider ?", speaker_wav=MEDIA_PATH+"pierre.wav", language="fr-fr", file_path=MEDIA_PATH+"output_FR.wav")
# tts.tts_to_file("Isso é clonagem de voz.", speaker_wav=MEDIA_PATH+"pierre.wav", language="pt-br", file_path=MEDIA_PATH+"output_PT.wav")