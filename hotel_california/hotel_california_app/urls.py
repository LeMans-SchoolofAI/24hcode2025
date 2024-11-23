from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('setup/', views.setup_view, name='setup_view'),
    path('reset/', views.reset_view, name='reset_view'),
]