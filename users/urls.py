from django.urls import path
from .views import register_api, register_page
from . import views
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('api/register/', register_api, name='api-register'),  
    path('register/', register_page, name='register'),
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow-user'),         
]
