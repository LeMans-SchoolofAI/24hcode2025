from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import whisper, os, ast, torch
from tempfile import NamedTemporaryFile
import warnings
from .models import Conversation, User_input, Ai_response
from .concierge import ask_AI
from TTS.api import TTS

# Ignorer les FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

model_whisper = whisper.load_model("base")

MEDIA_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))+ "/media/"  # just "/media" si docker
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True).to(device)



# Util function
def get_context(request):
    user_inputs = ast.literal_eval(request.POST.get("user_inputs")) if request.POST.get("user_inputs") != None else []
    ai_responses = ast.literal_eval(request.POST.get("ai_responses")) if request.POST.get("ai_responses") != None else []
    indices = list(range(len(ai_responses)))
    context = {
        "conversation_id": request.POST.get("conversation_id"),
        "user_inputs": user_inputs,
        "ai_responses": ai_responses,
        "indices": indices,
        "audio_url": request.POST.get("audio_url")
    }
    return context

def hello_world(request):
    return HttpResponse("Je suis un agent d'accueil virtuel pour les 24h du code. Je suis une intelligence artificielle développée par Le Mans School of AI.")

def index(request):
    if request.method == 'POST':
        context=get_context(request)
        return render(request, 'public_app/index.html', context=context)
    return render(request, 'public_app/index.html', context={})

def start_new_conversation(request):
    conversation_id = Conversation.objects.create().id
    ai_result = ask_AI(conversation_id, reset=True)
    ai_response = Ai_response.objects.create(position=0, response=ai_result["message"], conversation_id=conversation_id)
    
    # Text2speech
    audio_result_path = f"{MEDIA_PATH}conv_0_0.wav"
    if not os.path.exists(audio_result_path):
        tts.tts_to_file(ai_result["message"], 
                        speaker_wav=MEDIA_PATH+"pierre.wav", language="fr-fr", 
                        file_path=audio_result_path)
    
    context = {
        "conversation_id": conversation_id,
        "user_inputs": [],
        "ai_responses": [ai_response.response],
        "indices": [0],
        "audio_url": f"/media/conv_0_0.wav"
    }
    # Render a template with a form that auto-submits via JavaScript
    return render(request, 'public_app/redirect_post.html', context=context)
    
    

def audio_transcription_view(request):
    if request.method == 'POST':
        context=get_context(request)
        audio_file = request.FILES.get('audio')
        
        if not audio_file:
            return JsonResponse({"error": "No audio file provided"}, status=400)

        # Get the conversation id from the request
        conversation_id = context.get("conversation_id")
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                return JsonResponse({"error": "Conversation not found"}, status=404)
        else:
            return JsonResponse({"error": "No conversation id provided"}, status=400)

        # Enregistrer l'audio dans un fichier temporaire
        with NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
            temp_audio_file.write(audio_file.read())
            temp_audio_file.flush()  # S'assurer que tout est écrit sur le disque

            # Charger l'audio depuis le fichier temporaire et transcrire
            transcription = model_whisper.transcribe(temp_audio_file.name)
        
        transcription_text = transcription["text"]
        user_input = User_input.objects.create(position=conversation.user_input_set.count(), message=transcription_text, conversation=conversation)
        depth = user_input.position
        
        ai_result = ask_AI(conversation_id, user_question=transcription_text, depth=depth)
        if ai_result.get("stop"):
            return JsonResponse({"error": ai_result["message"]}, status=400)
        ai_response = Ai_response.objects.create(position=conversation.ai_response_set.count(), response=ai_result["message"], conversation=conversation)
        
        
        # Text2speech
        audio_result_path = f"{MEDIA_PATH}conv_{conversation_id}_{conversation.user_input_set.count()}.wav"
        tts.tts_to_file(ai_result["message"], 
                        speaker_wav=MEDIA_PATH+"pierre.wav", language="fr-fr", 
                        file_path=audio_result_path)
        
        
        context.update({
            "user_inputs": [ui.message for ui in conversation.user_input_set.all()],
            "ai_responses": [ar.response for ar in conversation.ai_response_set.all()],
            "indices": list(range(conversation.user_input_set.count())),
            "audio_url": f"/media/conv_{conversation_id}_{conversation.user_input_set.count()}.wav"
        })
        return render(request, 'public_app/redirect_post.html', context=context)
    else: # Not used, just to secure method by get
        return redirect('index')

# class AudioTranscriptionView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         audio_file = request.FILES.get('audio')
        
#         if not audio_file:
#             return Response({"error": "No audio file provided"}, status=400)

#         # Get the conversation id from the request
#         if request.data.get("conversation_id"):
#             conversation_id = request.data["conversation_id"]
#             conversation = Conversation.objects.get(id=conversation_id)
#         else:
#             return Response({"error": "No conversation id provided"}, status=400)

#         # Enregistrer l'audio dans un fichier temporaire
#         with NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio_file:
#             temp_audio_file.write(audio_file.read())
#             temp_audio_file.flush()  # S'assurer que tout est écrit sur le disque

#             # Charger l'audio depuis le fichier temporaire et transcrire
#             transcription = model_whisper.transcribe(temp_audio_file.name)
            
#         user_input = User_input.objects.create(position=conversation.user_input_set.count(), message=transcription, conversation=conversation)
#         ai_response = Ai_response.objects.create(position=conversation.ai_response_set.count(), response="Je suis une IA débile pour le moment", conversation=conversation)
            
#         context = {
#             "conversation_id": conversation_id,
#             "user_inputs": conversation.user_input_set.all(),
#             "ai_responses": conversation.ai_response_set.all(),
#             "indexes": range(conversation.user_input_set.count())
#         }
#         return render(request, 'public_app/index.html',context=context)