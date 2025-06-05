from django.urls import path
from .views import register_api, register_page

urlpatterns = [
    path('api/register/', register_api, name='api-register'),  
    path('register/', register_page, name='register'),         
]
