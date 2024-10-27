from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    return HttpResponse("Je suis un agent d'accueil virtuel pour les 24h du code. Je suis une intelligence artificielle développée par Le Mans School of AI.")

