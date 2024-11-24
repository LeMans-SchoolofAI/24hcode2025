from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'hotel_california_app'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/login/', LoginView.as_view(template_name='login.html', next_page='home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='hotel_california_app:home'), name='logout'),
    path('setup/', views.setup_view, name='setup_view'),
    path('admin-reset/', views.reset_view, name='reset_view'),
    path('reset/', views.reset_user_view, name='reset_user_view'),
]