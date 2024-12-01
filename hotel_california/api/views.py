from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions, status
from django_filters import rest_framework as filters
from .serializers import RestaurantSerializer, ClientSerializer, ReservationSerializer, MealTypeSerializer, SpaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from hotel_california_app.models import Restaurant, Client, Reservation, MealType,Spa

@extend_schema(
    description="Liste tous les restaurants de l'hôtel",
    responses={200: RestaurantSerializer},
    tags=["restaurants"]
)
class RestaurantListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]    
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

@extend_schema(
    description="Liste tous les clients de l'hôtel",
    responses={200: ClientSerializer},
    tags=["clients"]
)
class ClientListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer

    # Limit the results to the current user
    def get_queryset(self):
        """
        Les clients retournés sont ceux uniquement ceux de l'utilisateur connecté
        """
        return Client.objects.filter(user=self.request.user)

@extend_schema(
    description="Liste tous les type de repas disponibles",
    responses={200: MealTypeSerializer},
    tags=["repas", "meal"]
)
class MealTypeListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer

class ReservationFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ['restaurant', 'meal', 'date_from', 'date_to']

class ReservationListCreateView(generics.ListCreateAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer
    filterset_class = ReservationFilter

    def get_queryset(self):
        """Return reservations for the current user"""
        return Reservation.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Liste toutes les réservations",
        description="Retourne la liste paginée de toutes les reservations",
        parameters=[],
        responses={
            status.HTTP_200_OK: ReservationSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Récupère la liste des réservations.
        """
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Save the reservation with the current user"""
        serializer.save(
            user=self.request.user,
            client=serializer.validated_data['client']  # Le client est déjà validé
        )

    @extend_schema(
        summary="Créer une nouvelle réservation",
        description="Crée une nouvelle réservation pour un restaurant",
        #request=ReservationSerializer,
        responses={
            status.HTTP_201_CREATED: ReservationSerializer,
            status.HTTP_400_BAD_REQUEST: None
        },
        examples=[
            OpenApiExample(
                'Réservation valide',
                value={
                    'client': 1,
                    'restaurant': 1,
                    'date': '2024-12-25',
                    'meal': 1,
                    'number_of_guests': 4,
                    'special_requests': 'Table près de la fenêtre'
                },
                description="Exemple d'une réservation valide"
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        """Ensure users can only access their own reservations"""
        return Reservation.objects.filter(user=self.request.user)

class SpaListAPI(APIView):
    def get(self, request):
        spas = Spa.objects.all()
        serializer = SpaSerializer(spas, many=True)
        return Response(serializer.data)
