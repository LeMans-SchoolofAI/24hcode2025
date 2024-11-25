from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .data import setup_datas, reset_datas, reset_user_datas

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
    if request.method == 'POST':
        reset_datas(full=True)
        return render(request, 'home.html', context = {"messages" : ["Datas reset"]})
    return render(request, 'admin_reset.html')

# Réinitialise la configuration pour un utilisateur
def reset_user_view(request):
    reset_user_datas(request.user)
    return render(request, 'home.html', context = {"messages" : ["User datas reset"]})
    

from django.shortcuts import render
from .models import Spa

def list_spas(request):
    """Vue pour afficher une liste de spas."""
    spas = Spa.objects.all()
    return render(request, 'spa_list.html', {'spas': spas})
