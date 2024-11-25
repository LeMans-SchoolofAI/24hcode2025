from django.contrib import admin

from .models import Conversation, User_input, Ai_response

admin.site.register(Conversation)
admin.site.register(User_input)
admin.site.register(Ai_response)
