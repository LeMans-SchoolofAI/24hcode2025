from .models import *
import json


def setup_datas(full=False):
    with open("hotel_california_app/datas.json") as f:
        datas = json.load(f)

    if full:
        # 15 team account users
        users = datas["users"]
        for user in users:
            CustomUser.objects.create_user(username=user["username"], password=user["password"], email=user["email"], api_key=user["API key"])
        print("Users created")
    
    
    return True
        
    
    
def reset_datas(full=False):
    if full:
        # Get all users except the superuser
        users = CustomUser.objects.filter(is_superuser=False)
        users.delete()
        print("All users deleted")
        
    setup_datas(full=full)
    return True
    