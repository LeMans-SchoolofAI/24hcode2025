from django.urls import path
from .views import *

urlpatterns = [
    path('', hello_world, name='hello_world'),
    path('setup/', setup_view, name='setup_view'),
    path('reset/', reset_view, name='reset_view'),
]