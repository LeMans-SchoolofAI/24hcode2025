from django.urls import path
from .views import *

urlpatterns = [
    # path('', hello_world, name='hello_world'),
    path('', index, name='index'),
    path('transcribe/', AudioTranscriptionView.as_view(), name='audio-transcription'),
]