from django.urls import path
from .views import get_user_profile, register_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('me/', get_user_profile, name='user_profile'),
]