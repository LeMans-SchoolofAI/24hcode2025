from django.urls import path
from .views import RestaurantListAPIView, ClientListAPIView, SpaListAPI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

app_name = 'api'

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'restaurants': reverse('api:restaurant-list', request=request),
            'clients': reverse('api:client-list', request=request),
        })

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('clients/', ClientListAPIView.as_view(), name='client-list'),
    path('spas/', SpaListAPI.as_view(), name='spa_list_api'),
]