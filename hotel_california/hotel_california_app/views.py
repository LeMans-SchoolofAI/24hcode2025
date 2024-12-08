from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .data import setup_datas, reset_datas, reset_user_datas
from .models import Spa, Restaurant

@login_required
def user_home_view(request):
    return render(request, 'user_home.html')


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
        return render(request, 'huser_home.html', context = {"messages" : ["Datas reset"]})
    return render(request, 'admin_reset.html')

# Réinitialise la configuration pour un utilisateur
def reset_user_view(request):
    reset_user_datas(request.user)
    return render(request, 'user_home.html', context = {"messages" : ["User datas reset"]})
    
def list_spas(request):
    """Vue pour afficher une liste de spas."""
    spas = Spa.objects.all()
    return render(request, 'spa_list.html', {'spas': spas})

def home_view(request):
    restaurants = Restaurant.objects.all()
    # Générer la liste des restaurants sous la forme de dictionnaire avec le nom et la description
    restaurants_list = [{'name': restaurant.name, 'description': restaurant.description} for restaurant in restaurants]

    context = {
        'hotel_name': "Hôtel California",
        'hotel_location': "Le Mans",
        'welcome_text': "Situé au cœur de la charmante ville du Mans, l'Hôtel California vous accueille dans un cadre exceptionnel où le luxe et le raffinement se rencontrent. Notre établissement cinq étoiles offre une expérience inoubliable, alliant confort moderne et élégance classique.",
        
        'restaurants_title': "Restaurants Gastronomiques",
        'restaurants_intro': "Découvrez nos restaurants exquis, chacun proposant une expérience culinaire unique :",
        'restaurants': restaurants_list,

        'spa_title': "Spa & Bien-être",
        'spa_description': "Notre spa luxueux est un sanctuaire de détente et de revitalisation. Offrez-vous un moment de pur bien-être avec nos soins personnalisés :",
        'spa_services': [
            "Massages thérapeutiques et relaxants",
            "Soin du visage exclusifs avec des produits haut de gamme",
            "Bain turc traditionnel et sauna",
            "Centre de fitness équipé des dernières technologies"
        ],
        'spa_therapist_note': "Nos thérapeutes professionnels sont dédiés à votre confort et à votre sérénité, vous garantissant une expérience régénératrice.",

        'activities_title': "Activités & Loisirs",
        'activities_intro': "À l'Hôtel California, nous proposons une multitude d'activités pour agrémenter votre séjour :",
        'activities': [
            {
                'name': "Visites Culturelles",
                'description': "Explorez le patrimoine historique du Mans avec des visites guidées personnalisées de la vieille ville et de la célèbre Cathédrale Saint-Julien."
            },
            {
                'name': "Excursions Œnologiques",
                'description': "Partez à la découverte des vignobles locaux et dégustez des vins d'exception dans un cadre pittoresque."
            },
            {
                'name': "Cours de Cuisine",
                'description': "Participez à des ateliers culinaires animés par nos chefs et apprenez les secrets de la gastronomie française."
            },
            {
                'name': "Golf & Tennis",
                'description': "Bénéficiez d'un accès exclusif à des terrains de golf et des courts de tennis de premier ordre à proximité de l'hôtel."
            }
        ],
        'concierge_note': "Notre concierge se fera un plaisir de personnaliser votre programme selon vos envies et vos centres d'intérêt.",

        'hotel_address': "123 Avenue de la Liberté, 72000 Le Mans, France",
        'phone': "+33 2 43 00 00 00",
        'email': "contact@hotelcalifornia.fr",
        'social_links': [
            {'name': "Facebook", 'url': "https://www.facebook.com/hotelcalifornia"},
            {'name': "Instagram", 'url': "https://www.instagram.com/hotelcalifornia"},
            {'name': "Twitter", 'url': "https://www.twitter.com/hotelcalifornia"}
        ]
    }
    
    return render(request, 'home.html', context)
