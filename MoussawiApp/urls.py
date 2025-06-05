from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views
from rest_framework import routers
from .views import PostViewSet

urlpatterns = [
    path('', PostListView.as_view(), name='MoussawiApp-home'),
     path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='MoussawiApp-about'),
]

router = routers.DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='api-post')

urlpatterns += router.urls
