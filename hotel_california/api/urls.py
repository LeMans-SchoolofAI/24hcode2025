from django.urls import path
from .views import RestaurantListAPIView, ClientListAPIView, MealTypeListAPIView, ReservationListCreateView, ReservationDetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

app_name = 'api'

class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'restaurants': reverse('api:restaurant-list', request=request),
            'clients': reverse('api:client-list', request=request),
            'meals': reverse('api:meal-list', request=request),
            'reservations': reverse('api:reservation-list', request=request),
            'reservation-detail': reverse('api:reservation-detail', request=request, kwargs={'pk': 1}),
        })

urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('restaurants/', RestaurantListAPIView.as_view(), name='restaurant-list'),
    path('clients/', ClientListAPIView.as_view(), name='client-list'),
    path('meals/', MealTypeListAPIView.as_view(), name='meal-list'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
]
