from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions, status, filters, mixins
from django_filters import rest_framework as DRFFilters
from watson import search as watson
from .serializers import RestaurantSerializer, ClientSerializer, ReservationSerializer, MealTypeSerializer, SpaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from hotel_california_app.models import Restaurant, Client, Reservation, MealType,Spa

###################################
# Restaurants
###################################
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
        summary="Lister tous les restaurants de l'hôtel",
        responses={200: RestaurantSerializer},
        tags=["restaurants"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

###################################
# Clients
###################################
class WatsonSearchFilter(filters.SearchFilter):
    search_param = 'search'  # Définir le paramètre de recherche
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get(self.search_param, '')
        if not search_term:
            return Client.objects.none()
        
        return watson.filter(queryset, search_term)

class ClientAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer
    filter_backends = [WatsonSearchFilter]
    search_fields = ['search_fields']

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Rechercher un client",
        description="Rechercher un client",
        parameters=[OpenApiParameter('search', 'Chaine de recherche', OpenApiParameter.QUERY)],
        responses={
            status.HTTP_200_OK: ClientSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Créer un client",
        description="Créer un client",
        responses={
            status.HTTP_201_CREATED: ClientSerializer,
            status.HTTP_400_BAD_REQUEST: None
        },
        examples=[
            OpenApiExample(
                'Client valide',
                value={
                    'name': 'John Doe',
                    'phone_number': '+1 (555) 123-4567',
                    'room_number': '205',
                    'special_requests': 'None'
                },
                description="Exemple d'un client valide"
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ClientDetailAPIView(generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Limite l'accès aux clients de l'utilisateur connecté
        """
        return Client.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Détailler un client",
        description="Retourne les informations détaillées d'un client",
        parameters=[],
        responses={
            status.HTTP_200_OK: ClientSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Modifier un client",
        description="Modifie les informations d'un client",
        parameters=[],
        responses={
            status.HTTP_200_OK: ClientSerializer
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer un client",
        description="Supprime un client",
        parameters=[],
        responses={
            status.HTTP_204_NO_CONTENT: None
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

###################################
# Meals (Repas)
###################################
@extend_schema(
    description="Liste tous les types de repas disponibles",
    responses={200: MealTypeSerializer},
    tags=["meals"]
)
class MealTypeListAPIView(generics.ListAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    queryset = MealType.objects.all()
    serializer_class = MealTypeSerializer

    @extend_schema(
        summary="Lister les types de repas",
        description="Retourne la liste des types de repas",
        parameters=[],
        responses={
            status.HTTP_200_OK: MealTypeSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

###################################
# Réservations
###################################
class ReservationFilter(DRFFilters.FilterSet):
    date_from = DRFFilters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = DRFFilters.DateFilter(field_name='date', lookup_expr='lte')
    client = DRFFilters.ModelChoiceFilter(
        queryset=lambda request: Client.objects.filter(user=request.user)
    )
    class Meta:
        model = Reservation
        fields = ['client', 'restaurant', 'meal', 'date_from', 'date_to']

class ReservationListCreateView(generics.ListCreateAPIView):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer
    filterset_class = ReservationFilter

    def get_queryset(self):
        """Return reservations for the current user"""
        return Reservation.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Lister les réservations",
        description="Retourne la liste paginée des reservations répondant aux critères",
        parameters=[],
        responses={
            status.HTTP_200_OK: ReservationSerializer
        }
    )
    def get(self, request, *args, **kwargs):
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

class ReservationDetailView(generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    # Only allow an authenticated user
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Ensure users can only access their own reservations"""
        return Reservation.objects.filter(user=self.request.user)
    
    @extend_schema(
        summary="Modifier une reservation",
        description="Modifie les informations d'une reservation",
        parameters=[],
        responses={
            status.HTTP_200_OK: ReservationSerializer
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        summary="Supprimer une reservation",
        description="Supprime une reservation",
        parameters=[],
        responses={
            status.HTTP_204_NO_CONTENT: None
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Modifier partiellement une reservation",
        description="Modifie partiellement les informations d'une reservation",
        parameters=[],
        responses={
            status.HTTP_200_OK: ReservationSerializer
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Détailler une reservation",
        description="Retourne les informations concernant une reservation",
        parameters=[],
        responses={
            status.HTTP_200_OK: ReservationSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

###################################
# Spas
###################################
@extend_schema(
    description="Liste tous les spas de l'hôtel",
    responses={200: SpaSerializer},
    tags=["spas"]
)
class SpaListAPI(APIView):
    @extend_schema(
        summary="Lister tous les spas de l'hôtel",
        description="Retourne la liste des spas",
        parameters=[],
        responses={
            status.HTTP_200_OK: SpaSerializer
        }
    )
    def get(self, request):
        spas = Spa.objects.all()
        serializer = SpaSerializer(spas, many=True)
        return Response(serializer.data)
