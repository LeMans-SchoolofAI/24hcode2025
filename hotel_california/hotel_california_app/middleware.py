from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import CustomUser

class APIKeyAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        apikey = request.headers.get('Authorization')
        if apikey:
            try:
                user = CustomUser.objects.get(apikey=apikey)
                request.user = user
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid API Key'}, status=401)
        else:
            #return JsonResponse({'error': 'API Key required'}, status=401) # Laisser les autres méthodes d'authentification gérer l'absence de clé
            pass
        
        