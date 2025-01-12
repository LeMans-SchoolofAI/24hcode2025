from django.urls import path
from .views import RestaurantListAPIView, ClientAPIView, ClientDetailAPIView, MealTypeListAPIView, ReservationListCreateView, ReservationDetailView, SpaListAPI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
app_name = 'api'

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'restaurants': reverse('api:restaurant-list', request=request),
            'clients': reverse('api:client', request=request),
            'clients-detail': reverse('api:client-detail', request=request, kwargs={'id': 1}),
            'reservations': reverse('api:reservation', request=request),
            'reservation-detail': reverse('api:reservation-detail', request=request, kwargs={'id': 1}),
            'meals': reverse('api:meal-list', request=request),
            'spas': reverse('api:spa-list', request=request),
        })

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('clients/', ClientAPIView.as_view(), name='client'),
    path('clients/<int:id>/', ClientDetailAPIView.as_view(), name='client-detail'),
    path('meals/', MealTypeListAPIView.as_view(), name='meal-list'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation'),
    path('reservations/<int:id>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('spas/', SpaListAPI.as_view(), name='spa-list'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url='/api/schema/'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url='/api/schema/'), name='redoc'),
]
