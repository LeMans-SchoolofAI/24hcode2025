from django.urls import path
from .views import RestaurantListAPIView, ClientListAPIView

urlpatterns = [
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('clients/', ClientListAPIView.as_view(), name='client-list'),
]