from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .data import setup_datas, reset_datas

@login_required
def home_view(request):
    return render(request, 'home.html')


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

