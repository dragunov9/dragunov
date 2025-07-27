from django.urls import path
from .views import register_api, register_page
from . import views

urlpatterns = [
    path('api/register/', register_api, name='api-register'),  
    path('register/', register_page, name='register'),
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow-user'),         
]
