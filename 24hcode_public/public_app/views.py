from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import whisper
from tempfile import NamedTemporaryFile

def hello_world(request):
    return HttpResponse("Je suis un agent d'accueil virtuel pour les 24h du code. Je suis une intelligence artificielle développée par Le Mans School of AI.")

def index(request):
    return render(request, 'public_app/index.html')


class AudioTranscriptionView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        # Charger le modèle Whisper
        model = whisper.load_model("base")

        # Enregistrer l'audio dans un fichier temporaire
        with NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
            temp_audio_file.write(audio_file.read())
            temp_audio_file.flush()  # S'assurer que tout est écrit sur le disque

            # Charger l'audio depuis le fichier temporaire et transcrire
            transcription = model.transcribe(temp_audio_file.name)
        
        # Renvoyer la transcription
        return Response({"transcription": transcription['text']})