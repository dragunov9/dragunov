from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostViewSet,
    LikeViewSet,
    CommentViewSet,
    NotificationViewSet
)
from . import views
from rest_framework import routers
from .views import mark_notification_read
from .views import CommentViewSet

urlpatterns = [
    path('', PostListView.as_view(), name='MoussawiApp-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='MoussawiApp-about'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/notifications/<int:pk>/read/', mark_notification_read, name='mark_notification_read'),
]

router = routers.DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='api-post')

router.register(r'api/likes', LikeViewSet, basename='api-like')
router.register(r'api/comments', CommentViewSet, basename='api-comment')
router.register(r'api/notifications', NotificationViewSet, basename='api-notification')

urlpatterns += router.urls
