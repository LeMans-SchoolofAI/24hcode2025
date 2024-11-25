from django.contrib import admin
from .models import *

admin.site.register(Restaurant)
admin.site.register(MealType)
admin.site.register(MenuItem)
admin.site.register(DailyMenu)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Spa)