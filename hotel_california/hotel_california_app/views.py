from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .data import setup_datas, reset_datas

def hello_world(request):
    return HttpResponse("Welcome to the Hotel California, such a lovely place !")



# Vérifier si l'utilisateur est un superutilisateur
def is_superuser(user):
    return user.is_authenticated and user.is_superuser

# Charge la configuration de l'application
def setup_view(request):
    if not is_superuser(request.user):
        raise PermissionDenied
    setup_datas()
    return HttpResponse("App is ready to use !")

# Réinitialise la configuration de l'application
def reset_view(request):
    if not is_superuser(request.user):
        raise PermissionDenied
    reset_datas(full=True)
    return HttpResponse("App is reset !")

