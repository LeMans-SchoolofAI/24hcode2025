from django.urls import path
from .views import *

urlpatterns = [
    # path('', hello_world, name='hello_world'),
    path('', index, name='index'),
    path('transcribe/', audio_transcription_view, name='audio-transcription'),
    path('new_conversation/', start_new_conversation, name='new_conversation'),
]