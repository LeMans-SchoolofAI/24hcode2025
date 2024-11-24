from django.contrib.auth.hashers import make_password
from .models import *
import json
from django.apps import apps


def setup_datas(full=False):
    if full:
        # Load the users
        with open("hotel_california_app/datas/users.json") as f:
            datas = json.load(f)
        for user in datas['CustomUser']:
            user['password'] = make_password(user['password'])
            CustomUser.objects.create(**user)

        # Load data shared between users
        with open("hotel_california_app/datas/global_datas.json") as f:
            datas = json.load(f)
        for key, values in datas.items():
            model_name = key.capitalize()
            model = apps.get_model('hotel_california_app', model_name)

            for value in values:
                model.objects.create(**value)
    
    # Load per user datas
    for user in CustomUser.objects.filter(is_superuser=False):
        with open("hotel_california_app/datas/user_datas.json") as f:
            datas = json.load(f)
        # Load clients
        for client in datas['client']:
            # Add the user to the record
            client['user'] = user
            Client.objects.create(**client)

        # Load reservations
        for reservation in datas['reservation']:
            # Add the user to the record
            reservation['user'] = user
            # Get the id of the client from the name and for that specific user
            reservation['client'] = Client.objects.get(name=reservation['client'], user=user)
            # Get the id of the restaurant from the name
            reservation['restaurant'] = Restaurant.objects.get(name=reservation['restaurant'])
            # Get the id of the meal from the name
            reservation['meal'] = MealType.objects.get(name=reservation['meal'])
            Reservation.objects.create(**reservation)

    return True
        
    
# Reset all the datas    
def reset_datas(full=False):
    if full:
        # Delete the shared datas
        shared_objects = [ "Restaurant", "MealType", "MenuItem", "DailyMenu", "DailyMenuItem" ]
        for model_name in shared_objects:
            model = apps.get_model('hotel_california_app', model_name.capitalize())
            model.objects.all().delete()
        print("Shared datas deleted")

        # Get all users except the superuser
        users = CustomUser.objects.filter(is_superuser=False)
        users.delete()
        print("All users deleted")
        
    setup_datas(full=full)
    return True


# Reset the datas for a specific user
def reset_user_datas(user):
    # Delete the datas
    Client.objects.filter(user=user).delete()
    Reservation.objects.filter(user=user).delete()
    return True
    