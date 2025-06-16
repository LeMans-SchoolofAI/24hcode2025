import os
import sounddevice as sd
from scipy.io.wavfile import write

MEDIA_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))+ "/media/"  # just "/media/" si docker


def enregistrer_voix_sans_pyaudio(nom_fichier, duree, taux_echantillonnage=44100):
    """
    Enregistre la voix en utilisant sounddevice et sauvegarde dans un fichier .wav.

    :param nom_fichier: Nom du fichier de sortie (avec extension .wav)
    :param duree: Durée de l'enregistrement en secondes
    :param taux_echantillonnage: Fréquence d'échantillonnage (par défaut 44100 Hz)
    """
    print("Enregistrement en cours...")
    # Enregistrement de l'audio
    audio = sd.rec(int(duree * taux_echantillonnage), samplerate=taux_echantillonnage, channels=1, dtype='int16')
    sd.wait()  # Attendre la fin de l'enregistrement
    print("Enregistrement terminé.")

    # Sauvegarde dans un fichier WAV
    write(MEDIA_PATH+nom_fichier, taux_echantillonnage, audio)
    print(f"Fichier enregistré : {nom_fichier}")

# Exemple d'utilisation
enregistrer_voix_sans_pyaudio("pierre.wav", duree=120)
